import uuid
import time
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class Assumption:
    assumption: str
    why_made: str
    confidence: str = "Low"
    requires_confirmation: bool = True
    provenance: str = "AI_INFERRED"

@dataclass
class Constraint:
    constraint: str
    type: str
    provenance: str = "USER_STATED"
    confidence: str = "High"

@dataclass
class ResearchSpecification:
    project_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    specification_version: int = 1
    research_domain: List[str] = field(default_factory=lambda: ["General Research"])
    objective: Optional[str] = None
    expected_outcome: Optional[str] = None
    requirements: List[str] = field(default_factory=list)
    constraints: List[Constraint] = field(default_factory=list)
    existing_knowledge: List[str] = field(default_factory=list)
    unknowns: List[str] = field(default_factory=list)
    relationships: List[str] = field(default_factory=list)
    contradictions: List[str] = field(default_factory=list)
    assumptions: List[Assumption] = field(default_factory=list)
    success_criteria: List[str] = field(default_factory=list)
    user_preferences: Dict[str, Any] = field(default_factory=dict)
    available_resources: List[str] = field(default_factory=list)
    proposed_resources: List[str] = field(default_factory=list)
    unresolved_questions: List[str] = field(default_factory=list)
    provenance: Dict[str, str] = field(default_factory=dict)
    confidence: Dict[str, str] = field(default_factory=dict)
    update_history: List[Dict[str, Any]] = field(default_factory=list)
    machinery_detected: List[Dict[str, Any]] = field(default_factory=list)
    tools_detected: List[str] = field(default_factory=list)

class PrimaryUnderstandingEngine:
    """Robust Primary Understanding Engine (Layer 1) supporting continuous state, provenance, and corrections."""

    def __init__(self):
        self.spec = ResearchSpecification()
        self.conversation_history: List[str] = []

    def parse_input(self, user_message: str) -> ResearchSpecification:
        msg = user_message.strip()
        self.conversation_history.append(msg)
        self.spec.specification_version += 1

        is_correction = any(k in msg.lower() for k in ["correction:", "i don't want", "instead", "rather than", "i only want"])
        
        lower_msg = msg.lower()
        if not self.spec.objective or is_correction:
            if is_correction:
                self.spec.objective = msg
                self.spec.update_history.append({
                    "version": self.spec.specification_version,
                    "action": "CORRECTION",
                    "message": msg,
                    "timestamp": time.time()
                })
            else:
                self.spec.objective = msg
                self.spec.provenance["objective"] = "USER_STATED"
                self.spec.confidence["objective"] = "High"
                self.spec.update_history.append({
                    "version": self.spec.specification_version,
                    "action": "UPDATE",
                    "message": msg,
                    "timestamp": time.time()
                })
        else:
            self.spec.update_history.append({
                "version": self.spec.specification_version,
                "action": "PROGRESSIVE_UPDATE",
                "message": msg,
                "timestamp": time.time()
            })

        domains = []
        if any(w in lower_msg for w in ["flood", "rain", "water", "climate", "environmental"]):
            domains.append("Environmental Science & Hydrology")
        if any(w in lower_msg for w in ["display", "3d", "glasses-free", "optics"]):
            domains.append("Optical Engineering & Display Systems")
        if any(w in lower_msg for w in ["battery", "solar", "insulation", "building"]):
            domains.append("Materials Science & Energy Systems")
        if any(w in lower_msg for w in ["robot", "navigation", "algorithm", "prediction"]):
            domains.append("Computer Science & Artificial Intelligence")
        
        if domains:
            self.spec.research_domain = list(set(self.spec.research_domain + domains))

        if "affordable" in lower_msg or "low-cost" in lower_msg or "cheap" in lower_msg:
            self.spec.constraints.append(Constraint(
                constraint="Affordable / Low-cost",
                type="Qualitative Cost Constraint",
                provenance="USER_STATED",
                confidence="High"
            ))

        if "data" in lower_msg or "records" in lower_msg:
            self.spec.available_resources.append(msg)

        if "flood" in lower_msg and "historical" not in lower_msg and "labels" not in lower_msg:
            self.spec.unknowns.append("Missing historical training labels / ground truth data")

        if len(msg.split()) < 3 and not any(w in lower_msg for w in ["flood", "display", "battery"]):
            self.spec.unresolved_questions.append("Research objective is ambiguous. Please clarify specific goals.")

        self.spec.machinery_detected = [{"name": "Standard Research Workstation", "properties": {"Status": "Active"}}]
        self.spec.tools_detected = ["Python Scientific Stack", "Local Engine"]

        return self.spec
