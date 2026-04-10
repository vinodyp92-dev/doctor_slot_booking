from datetime import datetime, time, timedelta
from models import Slot
from db import SessionLocal

def generate_slots_for_date(date):
    db = SessionLocal()

    day = date.strftime("%A")

    if day == "Sunday":
        return

    timings = [
        (time(11, 0), time(14, 0)),
        (time(16, 30), time(20, 0))
    ]

    for start, end in timings:
        current = datetime.combine(date, start)
        end_dt = datetime.combine(date, end)

        while current < end_dt:
            exists = db.query(Slot).filter(
                Slot.date == date,
                Slot.time == current.time()
            ).first()

            if not exists:
                db.add(Slot(date=date, time=current.time()))

            current += timedelta(minutes=15)

    db.commit()
    db.close()