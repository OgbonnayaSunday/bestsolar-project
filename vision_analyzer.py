from google.cloud import vision
import io

def analyze_with_google_vision(image_path: str):
    """Analyze a roof image and estimate solar installation potential."""
    client = vision.ImageAnnotatorClient()

    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.object_localization(image=image)
    objects = response.localized_object_annotations

    print(f"✅ Detected {len(objects)} objects")

    # Simulate results
    roof_detected = any("roof" in obj.name.lower() or "building" in obj.name.lower() for obj in objects)

    if not roof_detected:
        return {
            "status": "no_roof_detected",
            "message": "No rooftop detected — try a clearer image."
        }

    # Rough estimate (example logic)
    num_panels = len(objects) * 4
    total_power = num_panels * 400
    battery_capacity = total_power * 5 / 1000
    charge_controller = total_power * 1.2 / 12

    return {
        "status": "success",
        "roof_area_m2": round(num_panels * 1.6, 2),
        "num_panels": num_panels,
        "total_power_watts": total_power,
        "battery_capacity_kwh": round(battery_capacity, 2),
        "charge_controller_rating": f"{int(charge_controller)}W"
    }
