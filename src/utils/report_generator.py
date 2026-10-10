import os

def generate_markdown_report(title: str, spec: dict, sources: list, metrics: dict) -> str:
    report_content = f"""# AI Research Lab - Project Report
**Project Title:** {title}
**Evidence Level:** Science-based Simulation

---

## 1. Research Specification (Layer 1)
- **Objective:** {spec.get('objective', 'N/A')}
- **Requirements:** Glasses-free 3D visual reconstruction

---

## 2. Retrieved Academic Sources (Layer 3)
"""
    for idx, src in enumerate(sources, 1):
        report_content += f"{idx}. **{src.get('title')}**\n"
        report_content += f"   - *Authors:* {src.get('authors_or_org')}\n"
        report_content += f"   - *Link:* {src.get('url')}\n"
        report_content += f"   - *Summary:* {src.get('summary')}\n\n"

    report_content += f"""---

## 3. Physical Simulation Metrics (Layer 4)
- **Laser Output Power:** {metrics.get('power_watts', 'N/A')} W
- **Calculated Optical Intensity:** {metrics.get('intensity_w_m2', 'N/A')} W/m²
- **Fresnel Diffraction Number:** {metrics.get('fresnel_number', 'N/A')}

---
*Generated locally by AI Research & 3D Simulation Workspace.*
"""
    os.makedirs("reports", exist_ok=True)
    filename = f"reports/{title.replace(' ', '_').lower()}_report.md"
    with open(filename, "w") as f:
        f.write(report_content)
    
    return filename
