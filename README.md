# 🩸 Blood Donation Backend

Welcome to the Blood Donation Backend! This is a simple, beginner-friendly REST API built with **FastAPI** and **PostgreSQL**. 

This platform connects blood donors with people in need. It provides a robust, optimized system for user authentication, location filtering, and donor availability management.

---

## 🚀 Getting Started (Beginner Friendly)

Follow these simple steps to run this project on your local machine.

### 1. Requirements
Make sure you have the following installed:
- Python 3.12+
- PostgreSQL
- [uv](https://github.com/astral-sh/uv) (for ultra-fast Python package management)

### 2. Setup the Environment
1. Clone this project and navigate into it.
2. Create and activate a virtual environment (optional but recommended):
   ```bash
   uv venv
   source .venv/bin/activate
   ```
3. Install the required dependencies:
   ```bash
   uv pip install -r pyproject.toml
   # OR just run:
   uv sync
   ```

### 3. Database Configuration
1. Open PostgreSQL and create a database named `blood_donation`.
2. Create a `.env` file in the root folder (where `main.py` is located) with your database credentials:
   ```env
   DATABASE_URL=postgresql+psycopg://username:password@localhost:5432/blood_donation
   SECRET_KEY=mysecretkey
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

### 4. Database Setup & Seeding
We need to create the tables into the database. Run the following command:
```bash
uv run python reset_db.py     # Drops old tables and creates fresh new tables
```

### 5. Run the Server
Finally, start up the FastAPI development server:
```bash
uv run fastapi dev app/main.py
```
Open your browser and navigate to **http://127.0.0.1:8000/docs** to see the interactive API documentation!

---

## 📁 Project Structure

This project follows a clean, layered architecture, making it easy to understand and extend.

```text
blood-donation-backends/
│
├── app/
│   ├── models/           # SQLAlchemy Database Models (Tables)
│   │   ├── user.py
│   │   └── request.py
│   │
│   ├── routes/           # API Endpoints (Controllers)
│   │   ├── auth_routes.py
│   │   ├── user_routes.py
│   │   ├── donor_routes.py
│   │   ├── request_route.py
│   │   ├── location_routes.py
│   │   └── blood_group_routes.py
│   │
│   ├── services/         # Business Logic & Database Queries
│   │   ├── auth_service.py
│   │   ├── donor_service.py
│   │   ├── request_service.py
│   │   ├── location_service.py
│   │   └── blood_group_service.py
│   │
│   ├── schemas/          # Pydantic Models for Data Validation (Request/Response)
│   │   ├── auth_schema.py
│   │   ├── user_schema.py
│   │   ├── donor_schema.py
│   │   ├── request_schema.py
│   │   ├── location_schema.py
│   │   └── blood_group_schema.py
│   │
│   ├── dependencies/     # Shared dependencies (like checking login tokens)
│   │   └── auth.py
│   │
│   ├── database.py       # Database Connection Setup
│   ├── config.py         # Environment Variables loading
│   └── main.py           # Application Entry Point
│
├── data/                 # Static JSON data for Locations & Blood Groups
├── reset_db.py           # Script to quickly recreate DB tables
```

> **Note on Static Data**: For optimal performance, location data (Divisions, Districts, Upazilas) and Blood Groups are served directly from the static JSON files in the `data/` folder, rather than putting them in the database!

---

## 🔌 API Design

Here is the list of available endpoints.

### Authentication & Users
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login to get an access token
- `GET /users/me` - Get my profile information
- `PUT /users/me` - Update my profile information

### Location APIs (Served from JSON Data)
- `GET /locations/divisions` - List all divisions
- `GET /locations/divisions/{division_id}/districts` - Get districts under a division
- `GET /locations/districts/{district_id}/upazilas` - Get upazilas under a district

### Blood Groups
- `GET /blood-groups` - List all blood groups (A+, A-, B+, B-, AB+, AB-, O+, O-)

### Donors
- `GET /donors` - Search for available donors
  - **Query Params**: `blood_group_id` (required), `district_id` (required), `upazila_id` (optional)
- `GET /donors/{id}` - View a specific donor's profile
- `PATCH /donors/me/availability` - Toggle your donor availability status
- `PATCH /donors/me/donated` - Mark that you just donated blood (auto-disables availability)

### Requests
- `POST /requests` - Create a new blood request
- `GET /requests` - Search open blood requests
  - **Query Params**: `blood_group_id` (optional), `district_id` (optional)
- `PATCH /requests/{id}/fulfill` - Mark a request as fulfilled/completed

---

## 📊 Database ER Diagram

Here is how the data is stored relationally in PostgreSQL. Notice how `division_id`, `district_id`, and `upazila_id` are stored strictly as Integers referencing the JSON data files.

```mermaid
erDiagram
    USERS {
        int id PK
        varchar name
        varchar email "Unique"
        varchar phone "Unique"
        varchar password
        int blood_group_id
        int division_id
        int district_id
        int upazila_id
        date last_donation_date
        boolean is_available
        timestamp created_at
    }

    BLOOD_REQUESTS {
        int id PK
        varchar requester_name
        varchar requester_phone
        varchar patient_name
        varchar hospital
        int blood_group_id
        int division_id
        int district_id
        int upazila_id
        int units_needed
        date needed_by
        varchar status
        timestamp created_at
    }
```

Happy coding! 🎉