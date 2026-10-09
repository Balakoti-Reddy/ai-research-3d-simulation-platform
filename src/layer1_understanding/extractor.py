from src.models.spec import ResearchSpecification, SpecItem, KnowledgeStatus

class PrimaryUnderstandingEngine:
    """Layer 1: Extracts and continuously updates key values in the user's natural language input."""

    def __init__(self, current_spec: ResearchSpecification = None):
        self.spec = current_spec or ResearchSpecification()

    def parse_input(self, user_text: str) -> ResearchSpecification:
        """
        Parses user text and updates the specification.
        (In production, connect this layer to an LLM structured output / JSON mode).
        """
        if not self.spec.objective:
            self.spec.objective = SpecItem(value=user_text, status=KnowledgeStatus.USER_STATED)
        else:
            self.spec.requirements.append(SpecItem(value=user_text, status=KnowledgeStatus.USER_STATED))
        
        return self.spec
