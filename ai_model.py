# ai_model.py
from PIL import Image
import math

def analyze_image_light(image_path):
    """
    Estimate solar setup from building image.
    This is a simple algorithm for Railway free deployment.
    """
    try:
        img = Image.open(image_path)
        width, height = img.size

        # Estimate roof area (in m²)
        roof_area = round((width * height) / 50000, 2)

        # Panels needed (1 panel ≈ 2 m²)
        num_panels = max(1, int(roof_area / 2))

        # Total power output (0.45 kW per panel)
        total_power_kw = round(num_panels * 0.45, 2)

        # Inverter, battery, controller
        inverter_kw = round(total_power_kw * 1.3, 2)
        battery_kwh = round(total_power_kw * 2.5, 2)
        charge_controller_amp = int(total_power_kw * 20)

        # Estimated cost (₦145,000 per panel)
        estimated_cost_naira = num_panels * 145000

        return {
            "roof_area_m2": roof_area,
            "num_panels": num_panels,
            "total_power_kw": total_power_kw,
            "inverter_kw": inverter_kw,
            "battery_kwh": battery_kwh,
            "charge_controller_amp": charge_controller_amp,
            "estimated_cost_naira": estimated_cost_naira
        }
    except Exception as e:
        return {"error": str(e)}
