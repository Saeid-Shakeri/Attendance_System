# سیستم حضور و غیاب (Attendance System)

## 🏗️ معماری پروژه

این پروژه یک سیستم حضور و غیاب مبتنی بر معماری میکروسرویس است که شامل دو سرویس مستقل می‌باشد:

### سرویس‌ها:

1. **Auth Service** (پورت 8000)
   - مدیریت کاربران و احراز هویت
   - صدور توکن JWT
   - ثبت نام و لاگین کاربران

2. **Attendance Service** (پورت 8001)
   - ثبت ورود و خروج کارمندان
   - مشاهده گزارشات حضور و غیاب

### مدل‌های داده:

- **User**: اطلاعات کاربران (username, password, employee_id, is_admin)
- **AttendanceRecord**: رکوردهای حضور و غیاب (employee_id, action, timestamp)

### امنیت:
- احراز هویت مبتنی بر JWT
- کاربران عادی فقط به داده‌های خود دسترسی دارند
- ادمین‌ها به تمام داده‌ها دسترسی دارند

## 🚀 راه‌اندازی

### پیش‌نیازها:
- Python 3.9+
- PostgreSQL

### نصب و راه‌اندازی:

1. کلون کردن پروژه:
```bash
git clone https://github.com/Saeid-Shakeri/Attendance_System.git
cd Attendance-System
```

2. نصب dependencies:
```bash
# for Auth Service
cd auth_service
pip install -r requirements.txt

# for Attendance Service
cd ../attendance_service
pip install -r requirements.txt
```

3.  PostgreSQL ایجاد دیتابیس ها در:
```sql
CREATE DATABASE auth_db;
CREATE DATABASE attendance_db;
```

4. ساخت فایل `.env`  در هر دو سرویس:
```env
# auth_service/.env
DATABASE_URL=postgresql://username:password@localhost:5432/auth_db
JWT_SECRET_KEY=your-super-secret-key-12345-change-in-production
JWT_ALGORITHM=HS256

# attendance_service/.env
DATABASE_URL=postgresql://username:password@localhost:5432/attendance_db
AUTH_SERVICE_URL=http://localhost:8000
```

5. اجرای سرویس‌ها:
```bash
# ترمینال ۱ - Auth Service
cd auth_service/app
uvicorn main:app --reload --port 8000 

# ترمینال ۲ - Attendance Service
cd attendance_service/app
uvicorn main:app --reload --port 8001
```

## 📡 نمونه درخواست‌های REST با curl

### 1. ثبت کاربر جدید
```bash
curl -X POST "http://localhost:8000/register"   
-H "Content-Type: application/json"   
-d '{
    "username": "user1",
    "password": "password123",
    "is_admin": false
  }'
```

### 2. دریافت توکن
```bash
curl -X POST "http://localhost:8000/token"   
-H "Content-Type: application/x-www-form-urlencoded"
-d "username=admin&password=adminpassword"
```

### 3. مشاهده اطلاعات کاربر جاری
```bash
curl -X GET "http://localhost:8000/users/me"
-H "Authorization: Bearer <YOUR_TOKEN>"
```

### 4. ثبت ورود
```bash
curl -X POST "http://localhost:8001/attendance"
-H "Authorization: Bearer <YOUR_TOKEN>"   
-H "Content-Type: application/json"   
-d '{
    "employee_id": 10,
    "action": "in"
  }'
```

### 5. ثبت خروج
```bash
curl -X POST "http://localhost:8001/attendance"
-H "Authorization: Bearer <YOUR_TOKEN>"
-H "Content-Type: application/json"
-d '{
    "employee_id": 10,
    "action": "out"
  }'
```

### 6. مشاهده رکوردهای خود کاربر
```bash
curl -X GET "http://localhost:8001/attendance/10"
-H "Authorization: Bearer <YOUR_TOKEN>"
```

### 7. مشاهده تمام رکوردها (فقط ادمین)
```bash
curl -X GET "http://localhost:8001/attendance"
-H "Authorization: Bearer <YOUR_TOKEN>"
```

## 🔐 نقش‌ها و دسترسی‌ها

### کاربر عادی:
- فقط می‌تواند برای خودش ثبت حضور/خروج انجام دهد
- فقط می‌تواند رکوردهای خودش را مشاهده کند

### کاربر ادمین:
- می‌تواند برای هر کارمندی ثبت حضور/خروج انجام دهد
- می‌تواند تمام رکوردهای سیستم را مشاهده کند

## 📋 endpoints  

### Auth Service (8000)
- `POST /token` - دریافت توکن JWT
- `POST /register` - ثبت نام کاربر جدید
- `GET /users/me` - اطلاعات کاربر جاری

### Attendance Service (8001)
- `POST /attendance` - ثبت ریکورد حضور/خروج
- `GET /attendance/{employee_id}` - مشاهده رکوردهای یک کارمند (توسط خودش و ادمین)
- `GET /attendance` - مشاهده تمام رکوردها (ادمین)
