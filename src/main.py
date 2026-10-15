import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from typing import Optional

from src.layer1_understanding.extractor import PrimaryUnderstandingEngine
from src.layer2_decision.decision_engine import ResearchDecisionEngine
from src.layer3_research.research_engine import ResearchSimulationEngine
from src.layer4_workspace.simulation_controls import InteractiveWorkspace
from src.utils.notebook_db import init_db, save_project
from src.utils.report_generator import generate_markdown_report

app = FastAPI(title="AI Research Lab")

init_db()

understanding_engine = PrimaryUnderstandingEngine()
decision_engine = ResearchDecisionEngine()
research_engine = ResearchSimulationEngine()
workspace = InteractiveWorkspace()

class UserInput(BaseModel):
    message: str

class ParamInput(BaseModel):
    laser_power_pct: Optional[float] = None
    image_size_m: Optional[float] = None

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/api/process")
async def process_user_input(payload: UserInput):
    updated_spec = understanding_engine.parse_input(payload.message)
    
    sources = []
    if updated_spec.objective:
        sources = research_engine.search_knowledge_base(updated_spec.objective)

    next_action = decision_engine.determine_next_action(updated_spec, sources)

    sources_data = [
        {
            "title": s.title,
            "authors_or_org": s.authors_or_org,
            "summary": s.summary,
            "url": s.url,
            "components": s.components
        } for s in sources
    ]

    save_project(
        title=updated_spec.objective,
        spec={"objective": updated_spec.objective, "tools_detected": updated_spec.tools_detected},
        sources=sources_data,
        params=workspace.params.__dict__
    )

    return {
        "spec": {
            "objective": updated_spec.objective,
            "tools_detected": updated_spec.tools_detected
        },
        "decision": next_action,
        "sources": sources_data
    }

@app.post("/api/parameters")
async def update_sim_parameters(params: ParamInput):
    res = workspace.calculate_optical_field(params.dict(exclude_none=True))
    return res

@app.get("/api/export-report")
async def export_report():
    obj_title = understanding_engine.spec.objective if understanding_engine.spec.objective else "Research Project"
    sources = research_engine.search_knowledge_base(obj_title)
    sources_data = [{"title": s.title, "authors_or_org": s.authors_or_org, "summary": s.summary, "url": s.url, "components": s.components} for s in sources]
    metrics = workspace.calculate_optical_field({})["metrics"]
    
    filepath = generate_markdown_report(obj_title, {"objective": obj_title, "tools": understanding_engine.spec.tools_detected}, sources_data, metrics)
    return FileResponse(filepath, filename=os.path.basename(filepath), media_type="text/markdown")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
