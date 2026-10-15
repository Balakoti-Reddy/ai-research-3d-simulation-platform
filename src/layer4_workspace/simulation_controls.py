from dataclasses import dataclass

@dataclass
class SimulationParams:
    laser_power_pct: float = 70.0
    image_size_m: float = 0.8

class InteractiveWorkspace:
    def __init__(self):
        self.params = SimulationParams()

    def calculate_optical_field(self, new_params: dict):
        if "laser_power_pct" in new_params:
            self.params.laser_power_pct = float(new_params["laser_power_pct"])
        if "image_size_m" in new_params:
            self.params.image_size_m = float(new_params["image_size_m"])

        power_w = round(5.0 * (self.params.laser_power_pct / 100.0), 2)
        intensity = round(power_w / max(0.1, (self.params.image_size_m ** 2 * 3.14159 / 4)), 2)
        fresnel = round((self.params.image_size_m ** 2) / (0.0006328 * 1.5), 1)

        return {
            "metrics": {
                "power_watts": power_w,
                "intensity_w_m2": intensity,
                "fresnel_number": fresnel
            }
        }
