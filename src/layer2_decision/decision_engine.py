from enum import Enum
from src.models.spec import ResearchSpecification

class ActionType(str, Enum):
    ASK_CLARIFICATION = "ask_clarification"
    RESEARCH_CONCEPTS = "research_concepts"
    EVALUATE_SIMULATOR = "evaluate_simulator"
    PROPOSE_PLAN = "propose_plan"

class ResearchDecisionEngine:
    """Layer 2: Decides the next action based on the extracted research spec."""

    def determine_next_action(self, spec: ResearchSpecification) -> dict:
        # Step 1: Check if core objective is missing
        if not spec.objective:
            return {
                "action": ActionType.ASK_CLARIFICATION,
                "question": "What is the primary objective or research question you want to explore?"
            }
        
        # Step 2: Check for unresolved critical ambiguities
        if spec.unknowns:
            return {
                "action": ActionType.ASK_CLARIFICATION,
                "question": f"To narrow down our research, could you clarify: {spec.unknowns[0].value}?"
            }

        # Step 3: Proceed with concept and tool research
        return {
            "action": ActionType.RESEARCH_CONCEPTS,
            "prompt": f"Search for existing papers, tools, and methods related to: {spec.objective.value}"
        }
