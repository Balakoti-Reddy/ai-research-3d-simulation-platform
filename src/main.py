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

HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Research Lab Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        body { background-color: #0B0F19; color: #94A3B8; font-family: system-ui, -apple-system, sans-serif; }
        .glass-panel { background: #111827; border: 1px solid #1E293B; border-radius: 12px; }
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-thumb { background: #334155; border-radius: 3px; }
    </style>
</head>
<body class="h-screen flex flex-col overflow-hidden text-sm">

    <header class="h-14 border-b border-slate-800 bg-slate-900/60 px-4 flex items-center justify-between shrink-0">
        <div class="flex items-center gap-3">
            <div class="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center text-white font-bold">AI</div>
            <div>
                <h1 class="font-semibold text-white leading-tight">AI Research Lab</h1>
                <p class="text-xs text-slate-500">Keyless Open Academic & Physical Workspace</p>
            </div>
        </div>
        <div>
            <button onclick="downloadReport()" class="bg-slate-800 border border-slate-700 text-slate-200 px-3 py-1.5 rounded-lg text-xs font-semibold hover:bg-slate-700 flex items-center gap-2">
                <i data-lucide="download" class="w-4 h-4"></i> Export Report
            </button>
        </div>
    </header>

    <div class="flex flex-1 overflow-hidden">
        <aside class="w-52 border-r border-slate-800 p-3 flex flex-col justify-between shrink-0">
            <nav class="space-y-1">
                <a href="#" class="flex items-center gap-3 px-3 py-2 rounded-lg bg-blue-600 text-white font-medium"><i data-lucide="layout-dashboard" class="w-4 h-4"></i> Research Workspace</a>
                <a href="#" class="flex items-center gap-3 px-3 py-2 rounded-lg text-slate-400 hover:bg-slate-800/50"><i data-lucide="compass" class="w-4 h-4"></i> Research Explorer</a>
            </nav>
        </aside>

        <main class="flex-1 p-4 grid grid-cols-12 gap-4 overflow-y-auto">
            <div class="col-span-3 space-y-4">
                <div class="glass-panel p-4 space-y-3">
                    <h2 class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Layer 1: Spec & Tools</h2>
                    <div>
                        <span class="text-[10px] text-slate-500 uppercase block">Objective</span>
                        <p id="spec-obj" class="text-xs text-white font-medium">None</p>
                    </div>
                    <div>
                        <span class="text-[10px] text-slate-500 uppercase block">Extracted Tools / Tech</span>
                        <div id="spec-tools" class="flex flex-wrap gap-1 mt-1">
                            <span class="text-xs text-slate-500 italic">None detected</span>
                        </div>
                    </div>
                </div>

                <div class="glass-panel p-4">
                    <h2 class="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Layer 3: Live arXiv Papers</h2>
                    <div id="sources-list" class="space-y-2 text-xs text-slate-400 max-h-72 overflow-y-auto">
                        <p class="italic">Enter an objective to query real arXiv papers...</p>
                    </div>
                </div>
            </div>

            <div class="col-span-6 glass-panel p-4 flex flex-col">
                <div class="flex items-center justify-between mb-3">
                    <h2 class="text-white font-semibold">Layer 4: Science Simulation</h2>
                    <span id="evidence-badge" class="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">Science-based Simulation</span>
                </div>

                <div id="canvas-container" class="flex-1 w-full min-h-[260px] rounded-lg bg-slate-950 overflow-hidden relative mb-3"></div>

                <div class="bg-slate-900 border border-slate-800 p-3 rounded-lg space-y-3">
                    <div class="grid grid-cols-3 gap-2 text-center text-xs pb-2 border-b border-slate-800">
                        <div>
                            <span class="text-slate-500 block">Optical Power</span>
                            <span id="calc-power" class="text-blue-400 font-mono font-semibold">3.5 W</span>
                        </div>
                        <div>
                            <span class="text-slate-500 block">Calculated Intensity</span>
                            <span id="calc-intensity" class="text-emerald-400 font-mono font-semibold">6.96 W/m²</span>
                        </div>
                        <div>
                            <span class="text-slate-500 block">Fresnel Number</span>
                            <span id="calc-fresnel" class="text-amber-400 font-mono font-semibold">802.0</span>
                        </div>
                    </div>

                    <div class="grid grid-cols-2 gap-4 text-xs pt-1">
                        <div>
                            <div class="flex justify-between text-slate-400 mb-1">
                                <span>Laser Power</span>
                                <span id="val-power" class="text-white font-mono">70%</span>
                            </div>
                            <input type="range" id="slider-power" min="10" max="100" value="70" oninput="updateParams()" class="w-full h-1 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-blue-500">
                        </div>
                        <div>
                            <div class="flex justify-between text-slate-400 mb-1">
                                <span>Image Scale</span>
                                <span id="val-scale" class="text-white font-mono">0.8m</span>
                            </div>
                            <input type="range" id="slider-scale" min="0.2" max="2.0" step="0.1" value="0.8" oninput="updateParams()" class="w-full h-1 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-blue-500">
                        </div>
                    </div>
                </div>
            </div>

            <div class="col-span-3 glass-panel p-4 flex flex-col justify-between">
                <div>
                    <h2 class="text-white font-semibold flex items-center gap-2 mb-3 border-b border-slate-800 pb-2">
                        <i data-lucide="sparkles" class="w-4 h-4 text-blue-400"></i> Research Assistant
                    </h2>
                    <div id="chat-messages" class="space-y-3 overflow-y-auto max-h-[calc(100vh-280px)] pr-1">
                        <div class="bg-blue-950/40 border border-blue-900/50 p-3 rounded-lg text-xs text-blue-200">
                            Type a prompt mentioning tools (e.g. "Research quantum computing using Python and Three.js") to see Layer 1 extract them!
                        </div>
                    </div>
                </div>

                <div class="mt-4 border-t border-slate-800 pt-3">
                    <div class="flex gap-2">
                        <input type="text" id="chat-input" placeholder="Search topic or tools..." class="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-blue-500">
                        <button onclick="handleSend()" class="bg-blue-600 text-white px-3 py-2 rounded-lg hover:bg-blue-500"><i data-lucide="send" class="w-4 h-4"></i></button>
                    </div>
                </div>
            </div>

        </main>
    </div>

    <script>
        lucide.createIcons();

        const container = document.getElementById('canvas-container');
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(60, container.clientWidth / container.clientHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ antialias: true });
        
        renderer.setSize(container.clientWidth, container.clientHeight);
        container.appendChild(renderer.domElement);

        const geometry = new THREE.OctahedronGeometry(1.2);
        const material = new THREE.MeshBasicMaterial({ color: 0x38bdf8, wireframe: true });
        const prism = new THREE.Mesh(geometry, material);
        scene.add(prism);

        camera.position.z = 3.5;

        function animate() {
            requestAnimationFrame(animate);
            prism.rotation.y += 0.008;
            renderer.render(scene, camera);
        }
        animate();

        async function updateParams() {
            const power = document.getElementById('slider-power').value;
            const scale = document.getElementById('slider-scale').value;

            document.getElementById('val-power').innerText = power + '%';
            document.getElementById('val-scale').innerText = scale + 'm';
            prism.scale.set(scale, scale, scale);

            const res = await fetch('/api/parameters', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ laser_power_pct: power, image_size_m: scale })
            });

            const data = await res.json();
            document.getElementById('calc-power').innerText = data.metrics.power_watts + ' W';
            document.getElementById('calc-intensity').innerText = data.metrics.intensity_w_m2 + ' W/m²';
            document.getElementById('calc-fresnel').innerText = data.metrics.fresnel_number;
        }

        async function handleSend() {
            const input = document.getElementById('chat-input');
            const messages = document.getElementById('chat-messages');
            const specObj = document.getElementById('spec-obj');
            const specTools = document.getElementById('spec-tools');
            const sourcesList = document.getElementById('sources-list');

            const text = input.value.trim();
            if (!text) return;

            messages.innerHTML += `<div class="bg-slate-800 p-2.5 rounded-lg text-xs text-slate-200"><strong>User:</strong> ${text}</div>`;
            input.value = '';

            try {
                const res = await fetch('/api/process', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: text })
                });

                if (!res.ok) throw new Error('Server returned status ' + res.status);

                const data = await res.json();
                specObj.innerText = data.spec.objective || 'None';

                specTools.innerHTML = data.spec.tools_detected.map(t => `
                    <span class="bg-blue-500/10 text-blue-400 border border-blue-500/20 px-2 py-0.5 rounded text-[10px] font-mono">${t}</span>
                `).join('');

                sourcesList.innerHTML = data.sources.map(s => `
                    <div class="p-2 bg-slate-900 border border-slate-800 rounded">
                        <a href="${s.url}" target="_blank" class="text-blue-400 font-semibold hover:underline">${s.title}</a>
                        <p class="text-[10px] text-slate-500">${s.authors_or_org}</p>
                        <p class="text-slate-300 mt-1">${s.summary}</p>
                    </div>
                `).join('');

                const assistantText = data.decision.question || data.decision.prompt || "Exploring research concepts...";
                messages.innerHTML += `
                    <div class="bg-slate-900 border border-slate-800 p-2.5 rounded-lg text-xs space-y-2">
                        <p class="text-emerald-400 font-semibold">[Layer 2 Decision Engine]</p>
                        <p class="text-slate-300">${assistantText}</p>
                    </div>
                `;
            } catch (err) {
                messages.innerHTML += `
                    <div class="bg-red-950 border border-red-900 p-2.5 rounded-lg text-xs text-red-300">
                        <strong>Error:</strong> Failed to process request (${err.message})
                    </div>
                `;
            }
            messages.scrollTop = messages.scrollHeight;
        }

        async function downloadReport() {
            window.open('/api/export-report', '_blank');
        }
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return HTML_LAYOUT

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
            "url": s.url
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
    sources_data = [{"title": s.title, "authors_or_org": s.authors_or_org, "summary": s.summary, "url": s.url} for s in sources]
    metrics = workspace.calculate_optical_field({})["metrics"]
    
    filepath = generate_markdown_report(obj_title, {"objective": obj_title, "tools": understanding_engine.spec.tools_detected}, sources_data, metrics)
    return FileResponse(filepath, filename=os.path.basename(filepath), media_type="text/markdown")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
