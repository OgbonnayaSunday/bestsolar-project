# ai_model.py
import math
from PIL import Image
import random

def analyze_image_light(image_path):
    # Load image
    img = Image.open(image_path)
    width, height = img.size

    # Simple roof area estimation (fake but realistic)
    roof_area = round((width * height) / 50000, 2)

    # Panels needed (1 panel = 2 m²)
    panels = max(1, int(roof_area / 2))

    # Solar output calculation
    total_kw = round(panels * 0.45, 2)  # 450W per panel

    inverter = round(total_kw * 1.3, 2)
    battery = round(total_kw * 2.5, 2)
    controller = int(total_kw * 20)
    cost = panels * 145000  # Naira

    return {
        "roof_area_m2": roof_area,
        "num_panels": panels,
        "total_power_kw": total_kw,
        "inverter_kw": inverter,
        "battery_kwh": battery,
        "charge_controller_amp": controller,
        "estimated_cost_naira": cost
    }
