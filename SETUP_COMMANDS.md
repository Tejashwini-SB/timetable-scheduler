# ============================================================
#  EduScheduler — PostgreSQL Setup & First Run Commands
#  Run these STEP BY STEP in your terminal
# ============================================================

# ─── STEP 1: Create PostgreSQL Database ─────────────────────
# Open psql or pgAdmin and run:
#
#   CREATE DATABASE timetable_db;
#   -- If using default postgres user, just update .env with the correct password

# ─── STEP 2: Update .env ────────────────────────────────────
# Edit .env and set your PostgreSQL password:
#   DB_PASSWORD=your_actual_postgres_password

# ─── STEP 3: Apply Migrations ───────────────────────────────
python manage.py migrate

# ─── STEP 4: Load Sample Data ───────────────────────────────
python manage.py load_sample_data

# ─── STEP 5: Start Server ───────────────────────────────────
python manage.py runserver

# Visit: http://127.0.0.1:8000
# Login: admin / admin123

# ─── OPTIONAL: Create your own superuser ────────────────────
python manage.py createsuperuser

# ─── OPTIONAL: Collect static files (for production) ────────
python manage.py collectstatic

# ─── PostgreSQL one-liner setup (Windows psql) ───────────────
# psql -U postgres -c "CREATE DATABASE timetable_db;"
