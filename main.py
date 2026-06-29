from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import sqlite3
from datetime import datetime

app = FastAPI(title="PAINT Booking API")

# CORS - frontend html file vera origin la irundhalum allow pannum
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # production la unga domain mattum podunga
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_NAME = "bookings.db"


def init_db():
    """Database & table create panrom (already irundha skip aagum)"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL,
            service TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            message TEXT,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


init_db()


# Request body structure - frontend la irundhu varura JSON match aaganum
class BookingRequest(BaseModel):
    name: str
    phone: str
    email: EmailStr
    service: str
    date: str
    time: str
    message: str | None = ""


@app.get("/")
def root():
    return {"status": "PAINT backend server running"}


@app.post("/api/book")
def create_booking(booking: BookingRequest):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO bookings (name, phone, email, service, date, time, message, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            booking.name,
            booking.phone,
            booking.email,
            booking.service,
            booking.date,
            booking.time,
            booking.message,
            datetime.now().isoformat()
        ))
        conn.commit()
        booking_id = cursor.lastrowid
        conn.close()

        return {
            "message": f"Booking confirmed for {booking.name} on {booking.date} at {booking.time}",
            "booking_id": booking_id
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Booking save aagavillai: {str(e)}")


@app.get("/api/bookings")
def get_all_bookings():
    """Admin ku - ella bookings um pakka idha use pannunga"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bookings ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()

    columns = ["id", "name", "phone", "email", "service", "date", "time", "message", "created_at"]
    bookings = [dict(zip(columns, row)) for row in rows]
    return {"total": len(bookings), "bookings": bookings}


@app.delete("/api/bookings/{booking_id}")
def delete_booking(booking_id: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM bookings WHERE id = ?", (booking_id,))
    conn.commit()
    deleted = cursor.rowcount
    conn.close()

    if deleted == 0:
        raise HTTPException(status_code=404, detail="Booking not found")
    return {"message": "Booking deleted"}
