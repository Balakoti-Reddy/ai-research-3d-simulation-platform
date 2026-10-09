from dataclasses import dataclass
from enum import Enum

class EvidenceLevel(str, Enum):
    CONCEPTUAL = "Conceptual Visualization"
    SCIENCE_BASED = "Science-based Simulation"
    CALIBRATED_TWIN = "Calibrated Digital Twin"
    PHYSICAL_EXP = "Physical Experiment"

@dataclass
class SimulationParameters:
    laser_power_pct: float = 70.0
    wavelength_nm: int = 532
    image_distance_m: float = 1.5
    image_size_m: float = 0.8
    show_light_path: bool = True

class InteractiveWorkspace:
    """Layer 4: Handles 3D workspace configuration, live parameters, and evidence guardrails."""

    def __init__(self):
        self.evidence_level = EvidenceLevel.CONCEPTUAL
        self.params = SimulationParameters()

    def update_parameters(self, new_params: dict) -> dict:
        """Updates model parameters while enforcing physical constraints."""
        if "laser_power_pct" in new_params:
            self.params.laser_power_pct = max(0.0, min(100.0, float(new_params["laser_power_pct"])))
        if "wavelength_nm" in new_params:
            self.params.wavelength_nm = int(new_params["wavelength_nm"])
        if "image_distance_m" in new_params:
            self.params.image_distance_m = float(new_params["image_distance_m"])
        if "image_size_m" in new_params:
            self.params.image_size_m = float(new_params["image_size_m"])

        return {
            "evidence_level": self.evidence_level.value,
            "parameters": self.params.__dict__,
            "warning": "Illustrative representation; not calculated from a validated scientific model." if self.evidence_level == EvidenceLevel.CONCEPTUAL else None
        }
