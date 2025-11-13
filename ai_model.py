# ai_model.py
import math
from ultralytics import YOLO
from PIL import Image

# Load pretrained or custom YOLO model
model = YOLO("yolov8n.pt")  # You can replace with your trained roof/solar model

def analyze_with_yolo(image_path: str):
    """
    Detect rooftop area and estimate solar installation size & cost.
    """
    results = model(image_path)
    detections = []
    total_area_px = 0

    for r in results:
        for box in r.boxes:
            cls = model.names[int(box.cls[0])]
            conf = float(box.conf[0])
            x1, y1, x2, y2 = box.xyxy[0]
            box_area = (x2 - x1) * (y2 - y1)
            total_area_px += box_area
            detections.append({
                "label": cls,
                "confidence": round(conf, 2),
                "area_px": round(box_area, 2)
            })

    # === Simulated conversion factor ===
    # You’ll tune this with calibration later.
    pixel_to_m2 = 0.0001
    roof_area_m2 = round(total_area_px * pixel_to_m2, 2)

    # === Solar Estimation Calculations ===
    if roof_area_m2 <= 0:
        roof_area_m2 = 50  # fallback default

    panel_size_m2 = 1.6  # average 400W panel size
    panel_watt = 400
    num_panels = int(roof_area_m2 / panel_size_m2)
    total_power_kw = (num_panels * panel_watt) / 1000

    inverter_kw = round(total_power_kw * 1.2, 2)
    battery_kwh = round(total_power_kw * 5, 2)
    controller_amp = round((num_panels * panel_watt) / 48, 2)
    estimated_cost_naira = round(total_power_kw * 1000 * 500, 2)

    return {
        "roof_area_m2": roof_area_m2,
        "num_panels": num_panels,
        "total_power_kw": round(total_power_kw, 2),
        "inverter_kw": inverter_kw,
        "battery_kwh": battery_kwh,
        "charge_controller_amp": controller_amp,
        "estimated_cost_naira": estimated_cost_naira,
        "detections": detections
    }
