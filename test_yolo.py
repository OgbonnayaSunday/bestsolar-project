from ultralytics import YOLO

# Load YOLO model
model = YOLO("yolov8n.pt")

# Run inference
results = model.predict(source="test.jpg", save=True, show=False)

# Print detection summary
for r in results:
    print("Detections:", r.boxes.xyxy)   # Bounding box coordinates
    print("Classes:", r.boxes.cls)       # Class IDs
    print("Confidences:", r.boxes.conf)  # Confidence scores
