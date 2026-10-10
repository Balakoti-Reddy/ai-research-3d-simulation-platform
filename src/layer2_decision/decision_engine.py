from enum import Enum
from typing import List

class ActionType(str, Enum):
    ASK_CLARIFICATION = "ask_clarification"
    RESEARCH_CONCEPTS = "research_concepts"
    EXPLORE_PAPER_SUB_TOPICS = "explore_paper_sub_topics"

class ResearchDecisionEngine:
    """Layer 2: Decides next actions and generates follow-up questions from retrieved papers."""

    def determine_next_action(self, spec, sources: List = None) -> dict:
        if not spec.objective:
            return {
                "action": ActionType.ASK_CLARIFICATION,
                "question": "What is the primary objective or research question you want to explore?"
            }
        
        if sources and len(sources) > 0:
            # Access attributes directly using dot notation instead of .get()
            paper_titles = [s.title for s in sources]
            suggested_focus = paper_titles[0] if paper_titles else "the core architecture"
            
            return {
                "action": ActionType.EXPLORE_PAPER_SUB_TOPICS,
                "question": f"Based on retrieved literature like '{suggested_focus}', would you like to investigate its underlying mathematical formulation or hardware constraints next?",
                "suggested_topics": paper_titles[:2]
            }

        return {
            "action": ActionType.RESEARCH_CONCEPTS,
            "prompt": f"Search for existing papers, tools, and methods related to: {spec.objective}"
        }
