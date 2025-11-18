# import cv2

# def detect_faces(image_path):
#     face_cascade = cv2.CascadeClassifier(
#         cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
#     )

#     img = cv2.imread(image_path)
#     if img is None:
#         return {"error": "Image not found or invalid format"}

#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#     faces = face_cascade.detectMultiScale(gray, 1.1, 4)

#     return {
#         "faces_detected": len(faces),
#         "faces": faces.tolist() if len(faces) > 0 else []
#     }
