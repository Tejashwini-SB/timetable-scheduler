# 🎓 EduScheduler — Automated Class Timetable Scheduler

A production-ready Django web application for educational institutions that automates class timetable scheduling with conflict detection, role-based access, and PDF/Excel export.

---

## 🚀 Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python 3.11+, Django 5.x |
| Database | PostgreSQL 15+ |
| Frontend | HTML5, Bootstrap 5.3, Vanilla CSS/JS |
| Auth | Django Auth + Role-based |
| Reports | ReportLab (PDF), OpenPyXL (Excel) |
| Server | Gunicorn + WhiteNoise |

---

## 📁 Project Structure

```
TimeTable/
├── timetable_scheduler/     ← Django project config
│   ├── settings.py
│   └── urls.py
├── accounts/                ← Auth, roles, user management
├── departments/             ← Departments, sections, academic years
├── faculty/                 ← Faculty management
├── subjects/                ← Subject management
├── classrooms/              ← Classroom management
├── timetable/               ← Core scheduler + conflict detection
├── reports/                 ← PDF/Excel export
├── templates/               ← HTML templates
├── static/                  ← CSS, JS, images
├── fixtures/                ← Sample data
├── .env                     ← Environment variables
└── requirements.txt
```

---

## ⚙️ Setup Instructions

### 1. Install PostgreSQL & Create Database

```sql
-- In psql:
CREATE DATABASE timetable_db;
CREATE USER timetable_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE timetable_db TO timetable_user;
```

### 2. Configure Environment

Edit `.env` file:
```
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=timetable_db
DB_USER=timetable_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Load Sample Data

```bash
python manage.py load_sample_data
```

### 6. Create Superuser (optional)

```bash
python manage.py createsuperuser
```

### 7. Run Development Server

```bash
python manage.py runserver
```

Visit: **http://127.0.0.1:8000**

---

## 🔐 Default Credentials (after sample data)

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin123` |
| Faculty | `dr.sharma` | `faculty123` |
| Faculty | `dr.patel` | `faculty123` |

---

## ✨ Key Features

### 1. Role-Based Access Control
- **Admin**: Full CRUD access to all modules
- **Faculty**: View-only access to timetables and own profile
- **Student**: View timetables

### 2. Auto-Scheduling Engine
Navigate to **Scheduling → Auto-Schedule** to:
1. Select a Section + Academic Year
2. Click "Generate Timetable"
3. The greedy algorithm assigns subjects → faculty → rooms → time slots without conflicts

### 3. Conflict Detection
- Faculty conflict: Same faculty in two places at the same time → blocked
- Classroom conflict: Same room double-booked → blocked
- Validation runs on every save (model-level `clean()`)

### 4. Reports & Export
- **PDF Timetable**: Color-coded grid layout
- **PDF Faculty Schedule**: Individual faculty schedule
- **Excel Export**: Styled workbook with merged cells
- **Classroom Utilization**: Usage statistics per room
- **Department Report**: Summary per department

---

## 📊 Database Schema

```
User (accounts) ──────────────────────────────────────┐
                                                       ↓
Department ──→ Section ──→ Timetable ──→ TimetableEntry
    ↓              ↑           ↑                ↓
Faculty ───────────┘     AcademicYear      TimeSlot
    ↓                                          ↑
Subject ──→ SubjectFacultyAssignment ──────────┘
                                           Classroom
```

---

## 🔧 Auto-Scheduler Prerequisites

Before running auto-schedule:
1. ✅ Add **Time Slots** (Scheduling → Time Slots)
2. ✅ Create **Subject-Faculty Assignments** (Scheduling → Assignments)
3. ✅ Add **Classrooms** with `is_available=True`
4. ✅ Create **Sections** under a Department + Academic Year

---

## 🌐 URL Routes

| URL | Description |
|-----|-------------|
| `/` | Redirect to dashboard |
| `/accounts/login/` | Login page |
| `/dashboard/` | Main dashboard |
| `/departments/` | Department management |
| `/faculty/` | Faculty management |
| `/subjects/` | Subject management |
| `/classrooms/` | Classroom management |
| `/timetable/` | Timetable list |
| `/timetable/auto-schedule/` | Auto-generator |
| `/timetable/assignments/` | Subject-Faculty assignments |
| `/timetable/timeslots/` | Time slot management |
| `/reports/` | Reports dashboard |
| `/admin/` | Django admin panel |

---

## 🚢 Production Deployment

```bash
# Set environment variables
DEBUG=False
ALLOWED_HOSTS=yourdomain.com

# Collect static files
python manage.py collectstatic

# Run with Gunicorn
gunicorn timetable_scheduler.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

---

## 📝 License

MIT License — Free to use for educational purposes.
