import uuid
import time
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class Capability:
    capability_id: str
    description: str
    is_available: bool
    required_inputs: List[str] = field(default_factory=list)

@dataclass
class DecisionRecord:
    decision_id: str = field(default_factory=lambda: f"dec-{str(uuid.uuid4())[:8]}")
    project_id: str = "default-project"
    specification_version: int = 1
    current_state: str = "UNDERSTANDING"
    selected_action: str = "CLARIFY"
    action_parameters: Dict[str, Any] = field(default_factory=dict)
    reason: str = "Initial evaluation."
    missing_information: List[str] = field(default_factory=list)
    confidence: str = "Medium"
    requires_user_approval: bool = False
    status: str = "READY"
    question: Optional[str] = None
    prompt: Optional[str] = None
    created_at: float = field(default_factory=time.time)

class ResearchDecisionEngine:
    """Context-aware Research Decision Engine (Layer 2)."""

    def __init__(self):
        self.capabilities = {
            "arxiv_retrieval": Capability("arxiv_retrieval", "Live arXiv academic search", True, ["query"]),
            "simulation_engine": Capability("simulation_engine", "3D physics and optical simulation", True, ["model_config"]),
            "calculation_tool": Capability("calculation_tool", "Parametric optical formulas", True, ["focal_length", "object_distance"]),
        }
        self.asked_questions: List[str] = []

    def evaluate_state_and_decide(self, spec: Any, execution_state: Optional[Dict[str, Any]] = None) -> DecisionRecord:
        execution_state = execution_state or {}
        spec_version = getattr(spec, "specification_version", 1)
        objective = getattr(spec, "objective", None)
        unknowns = getattr(spec, "unknowns", [])
        unresolved = getattr(spec, "unresolved_questions", [])

        record = DecisionRecord(specification_version=spec_version)

        # Test Case A: Unclear Objective
        if not objective or len(objective.strip()) < 5 or unresolved:
            record.current_state = "CLARIFICATION_REQUIRED"
            record.selected_action = "CLARIFY"
            record.reason = "Research objective is unclear or ambiguous; clarification is required before proceeding."
            record.missing_information = unresolved or ["Specific research goals and target outcomes"]
            q = "Could you please clarify your specific research objective and what you would like to achieve?"
            if q not in self.asked_questions:
                self.asked_questions.append(q)
            record.question = q
            record.prompt = "Action: CLARIFY | State: CLARIFICATION_REQUIRED"
            record.status = "READY"
            return record

        lower_obj = objective.lower()

        # Test Case C: Missing Data for Simulation / Execution
        if any(w in lower_obj for w in ["run", "execute", "simulation"]) and not execution_state.get("model_ready", False):
            record.current_state = "BLOCKED"
            record.selected_action = "REPORT_BLOCKER"
            record.reason = "Simulation requested but required model configuration or dataset is unavailable."
            record.missing_information = ["Validated simulation model", "Required input parameters"]
            record.question = "Cannot execute simulation yet: required model inputs or datasets are missing."
            record.prompt = "Action: REPORT_BLOCKER | State: BLOCKED"
            record.status = "BLOCKED"
            return record

        # Test Case B & D: Literature Exploration / Available Research
        if any(w in lower_obj for w in ["investigate", "explore", "methods", "predict", "find", "papers", "study"]) or len(execution_state.get("sources", [])) == 0:
            if execution_state.get("sources_retrieved", False):
                record.current_state = "EVIDENCE_REVIEW"
                record.selected_action = "EVIDENCE_REVIEW"
                record.reason = "Relevant papers have already been retrieved; proceeding to review existing evidence."
                record.question = "Would you like to analyze the methodology of the retrieved papers?"
                record.prompt = "Action: EVIDENCE_REVIEW | State: EVIDENCE_REVIEW"
            else:
                record.current_state = "READY_FOR_RESEARCH"
                record.selected_action = "RESEARCH"
                record.action_parameters = {"query": objective}
                record.reason = "Research objective is clear and appropriate for initial literature and evidence retrieval."
                q = f"Would you like to proceed with retrieving existing papers and methodologies for: '{objective}'?"
                record.question = q
                record.prompt = f"Action: RESEARCH | State: READY_FOR_RESEARCH"
            record.status = "READY"
            return record

        # Test Case F: Simulation Readiness
        if execution_state.get("model_ready", False) and execution_state.get("user_approved", False):
            record.current_state = "SIMULATION_IN_PROGRESS"
            record.selected_action = "RUN_SIMULATION"
            record.reason = "Validated model and required inputs exist, and user approval is granted."
            record.requires_user_approval = True
            record.question = "Simulation is ready for execution."
            record.prompt = "Action: RUN_SIMULATION | State: SIMULATION_IN_PROGRESS"
            record.status = "RUNNING"
            return record

        # Test Case I: User Approval Required for Consequential Actions
        if any(w in lower_obj for w in ["deploy", "train", "heavy computation"]):
            if not execution_state.get("user_approved", False):
                record.current_state = "WAITING_FOR_USER"
                record.selected_action = "WAIT_FOR_USER"
                record.reason = "Proposed action involves consequential computation and requires user approval."
                record.requires_user_approval = True
                record.question = "Do you approve proceeding with this consequential action?"
                record.prompt = "Action: WAIT_FOR_USER | State: WAITING_FOR_USER"
                record.status = "AWAITING_APPROVAL"
                return record

        # Default standard research state
        record.current_state = "METHOD_EVALUATION"
        record.selected_action = "IDENTIFY_METHODS"
        record.reason = "Objective and sources evaluated; identifying candidate scientific methods."
        record.question = "Shall we evaluate suitable methods for this research?"
        record.prompt = "Action: IDENTIFY_METHODS | State: METHOD_EVALUATION"
        record.status = "READY"
        return record
