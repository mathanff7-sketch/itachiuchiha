# PAINT Booking Backend - Setup Guide

## Idhu enna pannum?
Unga HTML file (madhan_html2.html) la irukura booking form, idha submit pannina
`http://localhost:5000/api/book` ku data anupum. Indha FastAPI backend adha
receive panni `bookings.db` (SQLite) file la save pannum.

## Setup Steps

### 1. Python install irukka check pannunga
```bash
python --version
```
(Python 3.9+ irukkanum)

### 2. Folder ku poyi dependencies install pannunga
```bash
cd paint_backend
pip install -r requirements.txt
```

### 3. Server start pannunga
```bash
uvicorn main:app --reload --port 5000
```

Idhu run aana udane terminal la idhu mathiri varum:
```
Uvicorn running on http://127.0.0.1:5000
```

### 4. HTML file open pannunga
`madhan_html2.html` file ah browser la open pannunga (double click).
Booking form fill panni submit pannunga - "Appointment Booked Successfully!"
alert varanum.

## Available Endpoints

| Method | URL                          | Vela enna pannum                  |
|--------|-------------------------------|------------------------------------|
| GET    | /                              | Server run aaguthu ah check         |
| POST   | /api/book                      | Pudhu booking create pannum        |
| GET    | /api/bookings                  | Ella bookings um list pannum       |
| DELETE | /api/bookings/{id}              | Specific booking delete pannum     |

## Bookings pakka venuma?
Browser la idha open pannunga: http://localhost:5000/api/bookings

## Auto Documentation (Swagger UI)
FastAPI free ah API testing page kudukum:
http://localhost:5000/docs

Idhu la nerukka ah API test pannalam, form fill panna theva illama.

## Important Notes
- `bookings.db` file automatic ah create aagum, first run la.
- Production ku deploy panna, CORS settings la `allow_origins=["*"]` ah
  unga actual domain ah change pannunga (security ku nalladhu).
- Database delete aaganum na, `bookings.db` file delete pannunga, automatic
  ah pudhusa create aagum.

## Trouble varudhu na?
- "Backend server run aagavillai" alert varudha? → Step 3 la server run
  pannirukkeengala nu check pannunga.
- Port already in use error varudha? → `--port 5001` mathiri vera port
  use pannunga, but HTML file la kuda andha port number change pannunga.
