import math
from dataclasses import dataclass
from enum import Enum

class EvidenceLevel(str, Enum):
    CONCEPTUAL = "Conceptual Visualization"
    SCIENCE_BASED = "Science-based Simulation"

@dataclass
class SimulationParameters:
    laser_power_pct: float = 70.0
    wavelength_nm: int = 532
    image_distance_m: float = 1.5
    image_size_m: float = 0.8

class InteractiveWorkspace:
    """Layer 4: Real-time mathematical simulation calculation without external key dependencies."""

    def __init__(self):
        self.params = SimulationParameters()

    def calculate_optical_field(self, new_params: dict) -> dict:
        """Calculates optical field intensity and diffraction geometry dynamically."""
        if "laser_power_pct" in new_params:
            self.params.laser_power_pct = float(new_params["laser_power_pct"])
        if "image_size_m" in new_params:
            self.params.image_size_m = float(new_params["image_size_m"])

        # Physical Wavefront Calculations
        wavelength_m = 532e-9  # Green laser wavelength
        power_watts = (self.params.laser_power_pct / 100.0) * 5.0  # 5W Max Output
        area_m2 = math.pi * ((self.params.image_size_m / 2.0) ** 2)
        
        # Intensity = Power / Area
        intensity_w_m2 = power_watts / max(area_m2, 0.001)

        # Fresnel Number (Determines diffraction region)
        fresnel_num = (self.params.image_size_m ** 2) / (wavelength_m * 1.5)

        return {
            "evidence_level": EvidenceLevel.SCIENCE_BASED.value if fresnel_num > 1.0 else EvidenceLevel.CONCEPTUAL.value,
            "metrics": {
                "intensity_w_m2": round(intensity_w_m2, 2),
                "power_watts": round(power_watts, 2),
                "fresnel_number": round(fresnel_num, 2)
            },
            "parameters": self.params.__dict__
        }
