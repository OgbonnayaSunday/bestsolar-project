from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, EmailStr
from database import Base, engine
from ai_model import analyze_image_light
from PIL import Image
from email.mime.text import MIMEText
import smtplib
import io
import math
from dotenv import load_dotenv
import os
import sqlite3
from datetime import datetime
from reportlab.pdfgen import canvas
load_dotenv()




Base.metadata.create_all(bind=engine)

# ==============================================
# 🚀 FastAPI App
# ==============================================
app = FastAPI()

# Allow frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================================
# ⚙️ Setup folders and database
# ==============================================
os.makedirs("static/uploads", exist_ok=True)

def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phone TEXT,
            address TEXT,
            propertyType TEXT,
            energyBill TEXT,
            timeframe TEXT,
            message TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()


# ==============================================
# 📬 Contact Form Schema
# ==============================================


class ContactForm(BaseModel):
    name: str
    email: EmailStr
    phone: str
    address: str
    propertyType: str
    energyBill: str
    timeframe: str = ""
    message: str = ""

@app.post("/contact")
async def receive_contact(form: ContactForm):
    try:
        print("📩 Received contact:", form.dict())

        # Save to database
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("""
            INSERT INTO notifications
            (name, email, phone, address, propertyType, energyBill, timeframe, message, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            form.name, form.email, form.phone, form.address,
            form.propertyType, form.energyBill, form.timeframe, form.message,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        conn.commit()
        conn.close()

        # ====== Send Email ======
        sender_email = os.getenv("EMAIL_USER")
        sender_pass = os.getenv("EMAIL_PASS")
        receiver_email = os.getenv("RECEIVER_EMAIL", sender_email)

        subject = f"🌞 New Solar Installation Request from {form.name}"
        body = f"""
        New Solar Request Received:

        Name: {form.name}
        Email: {form.email}
        Phone: {form.phone}
        Address: {form.address}
        Property Type: {form.propertyType}
        Energy Bill: {form.energyBill}
        Timeframe: {form.timeframe}
        Message: {form.message}

        📅 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """

        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = receiver_email

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_pass)
            server.send_message(msg)

        print("✅ Email sent successfully!")
        return {"message": "Form submitted, saved, and email sent successfully."}

    except Exception as e:
        print("❌ Email Error:", e)
        return {"message": "Form saved, but email sending failed.", "error": str(e)}
# ==============================================
# 🔔 Get Notifications (for admin dashboard)
# ==============================================
@app.get("/notifications")
def get_notifications():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM notifications ORDER BY id DESC")
    data = c.fetchall()
    conn.close()
    return {"notifications": data}

# ==============================================
# 🖼️ Analyze Image (Stable Version)
# ==============================================
# ======= Solar Estimation =======

@app.post("/estimate-solar/")
async def estimate_solar(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        file_path = f"static/uploads/{file.filename}"
        with open(file_path, "wb") as f:
            f.write(contents)

        result = analyze_image_light(file_path)
        return {"status": "success", "data": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==============================================
# 🧾 Generate PDF Report
# ==============================================
@app.get("/generate-pdf")
def generate_pdf():
    try:
        file_path = "static/uploads/solar_report.pdf"
        c = canvas.Canvas(file_path)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, 750, "🌞 Solar Installation Report")
        c.setFont("Helvetica", 12)
        c.drawString(100, 720, "This is a generated report about solar system setup.")
        c.drawString(100, 700, "Generated by BestSolar AI System.")
        c.save()

        if os.path.exists(file_path):
            return FileResponse(file_path, media_type="application/pdf", filename="solar_report.pdf")
        else:
            return JSONResponse(status_code=500, content={"error": "PDF not generated."})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# ==============================================
# 🏠 Root Route
# ==============================================
@app.get("/")
def root():
    return {"message": "✅ BestSolar Backend is running successfully 🚀"}
