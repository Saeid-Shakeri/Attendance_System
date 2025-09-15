# Attendance System

## 🏗️ Project Architecture

This project is an attendance system based on a microservice architecture, consisting of two independent services:

### Services:

1.  **Auth Service** (port 8000)
    -   User management and authentication
    -   Issuing JWT tokens
    -   User registration and login
2.  **Attendance Service** (port 8001)
    -   Logging employee check-in and check-out
    -   Viewing attendance reports

### Data Models:

-   **User**: User information (username, password, employee_id, is_admin)
-   **AttendanceRecord**: Attendance records (employee_id, action, timestamp)

### Security:

-   JWT-based authentication
-   Regular users can only access their own data
-   Admins can access all data

## 🚀 Setup

### Prerequisites:

-   Python 3.9+
-   PostgreSQL

### Installation and Setup:

1.  Clone the project:

``` bash
git clone https://github.com/Saeid-Shakeri/Attendance_System.git
cd Attendance-System
```

2.  Install dependencies:

``` bash
# for Auth Service
cd auth_service
pip install -r requirements.txt

# for Attendance Service
cd ../attendance_service
pip install -r requirements.txt
```

3.  Create PostgreSQL databases:

``` sql
CREATE DATABASE auth_db;
CREATE DATABASE attendance_db;
```

4.  Create `.env` file in both services:

``` env
# auth_service/.env
DATABASE_URL=postgresql://username:password@localhost:5432/auth_db
JWT_SECRET_KEY=your-super-secret-key-12345-change-in-production
JWT_ALGORITHM=HS256

# attendance_service/.env
DATABASE_URL=postgresql://username:password@localhost:5432/attendance_db
AUTH_SERVICE_URL=http://localhost:8000
```

5.  Run services:

``` bash
# Terminal 1 - Auth Service
cd auth_service/app
uvicorn main:app --reload --port 8000 

# Terminal 2 - Attendance Service
cd attendance_service/app
uvicorn main:app --reload --port 8001
```

## 📡 REST Request Examples with curl

### 1. Register a new user

``` bash
curl -X POST "http://localhost:8000/register"   
-H "Content-Type: application/json"   
-d '{
    "username": "user1",
    "password": "password123",
    "employee_id": 0,
    "is_admin": false
  }'
```

### 2. Get token

``` bash
curl -X POST "http://localhost:8000/token"   
-H "Content-Type: application/x-www-form-urlencoded"
-d "username=admin&password=adminpassword"
```

### 3. Get current user info

``` bash
curl -X GET "http://localhost:8000/users/me"
-H "Authorization: Bearer <YOUR_TOKEN>"
```

### 4. Log check-in

``` bash
curl -X POST "http://localhost:8001/attendance"
-H "Authorization: Bearer <YOUR_TOKEN>"   
-H "Content-Type: application/json"   
-d '{
    "employee_id": 10,
    "action": "in"
  }'
```

### 5. Log check-out

``` bash
curl -X POST "http://localhost:8001/attendance"
-H "Authorization: Bearer <YOUR_TOKEN>"
-H "Content-Type: application/json"
-d '{
    "employee_id": 10,
    "action": "out"
  }'
```

### 6. View user's own records

``` bash
curl -X GET "http://localhost:8001/attendance/10"
-H "Authorization: Bearer <YOUR_TOKEN>"
```

### 7. View all records (admin only)

``` bash
curl -X GET "http://localhost:8001/attendance"
-H "Authorization: Bearer <YOUR_TOKEN>"
```

## 🔐 Roles and Permissions

### Regular User:

-   Can only log check-in/out for themselves
-   Can only view their own records

### Admin User:

-   Can log check-in/out for any employee
-   Can view all system records

## 📋 Endpoints

### Auth Service (8000)

-   `POST /token` - Get JWT token
-   `POST /register` - Register new user
-   `GET /users/me` - Get current user info

### Attendance Service (8001)

-   `POST /attendance` - Log check-in/out record
-   `GET /attendance/{employee_id}` - View an employee's records (by
    themselves or admin)
-   `GET /attendance` - View all records (admin)
