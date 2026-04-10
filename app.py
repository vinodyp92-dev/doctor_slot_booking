from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import date

from db import Base, engine, SessionLocal
from models import User, Slot, Appointment
from otp import generate_otp, verify_otp
from scheduler import generate_slots_for_date
from whatsapp import send_whatsapp

app = FastAPI()
#templates = Jinja2Templates(directory="templates")
#templates = Jinja2Templates(directory="./templates")

import os
from fastapi.templating import Jinja2Templates

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
Base.metadata.create_all(bind=engine)

# Generate today's slots
generate_slots_for_date(date.today())


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )

@app.post("/send-otp")
def send(phone: str = Form(...), name: str = Form(...)):
    generate_otp(phone)
    return {"message": "OTP sent"}


@app.post("/verify")
def verify(phone: str = Form(...), otp: str = Form(...), name: str = Form(...)):
    if not verify_otp(phone, otp):
        return {"error": "Invalid OTP"}

    db = SessionLocal()
    user = db.query(User).filter(User.phone == phone).first()

    if not user:
        user = User(phone=phone, name=name)
        db.add(user)
        db.commit()

    return {"message": "Login success"}


@app.get("/slots")
def get_slots():
    db = SessionLocal()
    slots = db.query(Slot).filter(Slot.status == "available").all()

    return [{"id": s.id, "time": str(s.time)} for s in slots]


@app.post("/book")
def book(slot_id: int = Form(...), name: str = Form(...), phone: str = Form(...)):
    db = SessionLocal()

    slot = db.query(Slot).filter(Slot.id == slot_id).first()

    if slot.status == "booked":
        return {"error": "Already booked"}

    slot.status = "booked"

    db.add(Appointment(
        user_name=name,
        phone=phone,
        date=slot.date,
        time=slot.time
    ))

    db.commit()

    message = f"Appointment confirmed on {slot.date} at {slot.time}"
    send_whatsapp(phone, message)

    return {"message": "Booked successfully"}