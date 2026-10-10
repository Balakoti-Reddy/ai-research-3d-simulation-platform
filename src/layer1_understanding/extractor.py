from dataclasses import dataclass, field
from typing import List

@dataclass
class ResearchSpec:
    objective: str = "None"
    tools_detected: List[str] = field(default_factory=list)
    raw_text: str = ""

class PrimaryUnderstandingEngine:
    """Layer 1: Locally parses natural text to extract objectives and required tools/technologies."""

    def __init__(self):
        self.spec = ResearchSpec()

    def parse_input(self, text: str) -> ResearchSpec:
        cleaned = text.strip()
        if not cleaned:
            return self.spec

        self.spec.raw_text = cleaned
        self.spec.objective = cleaned

        # Local keyword scanning for tools & frameworks (Keyless & Offline)
        known_tools = [
            "python", "fastapi", "three.js", "sqlite", "opencv", 
            "pytorch", "tensorflow", "arxiv", "numpy", "scipy", 
            "tailwind", "markdown", "ollama", "react", "javascript"
        ]
        
        detected = []
        lower_text = cleaned.lower()
        for tool in known_tools:
            if tool in lower_text:
                detected.append(tool.capitalize())

        self.spec.tools_detected = detected if detected else ["Standard Library / Keyless APIs"]
        return self.spec
