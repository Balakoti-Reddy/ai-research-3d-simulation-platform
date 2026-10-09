from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

class KnowledgeStatus(str, Enum):
    USER_STATED = "user-stated"
    INFERRED = "inferred"
    RESEARCH_SUPPORTED = "research-supported"
    UNRESOLVED = "unresolved"

@dataclass
class SpecItem:
    value: str
    status: KnowledgeStatus = KnowledgeStatus.UNRESOLVED

@dataclass
class ResearchSpecification:
    objective: Optional[SpecItem] = None
    expected_outcome: Optional[SpecItem] = None
    requirements: List[SpecItem] = field(default_factory=list)
    constraints: List[SpecItem] = field(default_factory=list)
    existing_knowledge: List[SpecItem] = field(default_factory=list)
    unknowns: List[SpecItem] = field(default_factory=list)

    def is_ambiguous(self) -> bool:
        """Returns True if critical objective or expected outcome details are missing."""
        return self.objective is None or len(self.unknowns) > 0
