# University ERP System - Complete Setup Guide

## 🎓 Overview
This is a complete AI-powered University ERP system built with Django (backend) and React (frontend) that covers the entire student lifecycle from enrollment to graduation.

## 🏗️ System Architecture

### Backend (Django)
- **Framework**: Django 4.2.7 + Django REST Framework
- **Database**: SQLite3 (development) / MySQL (production)
- **Authentication**: JWT-based with role management
- **API**: RESTful endpoints for all modules

### Frontend (React)
- **Framework**: React 18 with TypeScript
- **Styling**: TailwindCSS for responsive UI
- **State Management**: Context API
- **HTTP Client**: Axios

### Core Modules
1. **Authentication** - JWT-based role management
2. **Students** - Enrollment, attendance, assignments, results
3. **Faculty** - Course management, workload, evaluations, research
4. **Exams** - Scheduling, question bank, grading, results
5. **Admissions** - Application process, document verification, tests
6. **Administration** - Announcements, committees, policies, grievances
7. **Backoffice** - Finance, HR, payroll, library, hostel, inventory

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Git

### Backend Setup (Django)

1. **Navigate to the project directory:**
   ```bash
   cd /Users/vivek/Documents/Code/ERP
   ```

2. **Activate virtual environment:**
   ```bash
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser:**
   ```bash
   python manage.py createsuperuser
   # Username: admin
   # Email: admin@university.edu
   # Password: admin123
   ```

6. **Start Django development server:**
   ```bash
   python manage.py runserver
   ```
   
   Backend will be available at: http://localhost:8000

### Frontend Setup (React)

1. **Navigate to frontend directory:**
   ```bash
   cd frontend_react
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start React development server:**
   ```bash
   npm start
   ```
   
   Frontend will be available at: http://localhost:3000

## 🔑 Demo Accounts

### Admin Access
- **Username**: admin
- **Password**: admin123
- **Role**: Administrator
- **Access**: Full system access including reports and analytics

### Sample User Types
The system supports the following user roles:
- **Student**: Course enrollment, assignments, grades, attendance
- **Faculty**: Course management, grading, research tracking
- **Admin**: System administration, user management
- **Management**: Analytics, reports, decision making
- **Staff**: Back-office operations

## 📊 Key Features

### Student Portal
- Personal dashboard with academic summary
- Course enrollment and tracking
- Assignment submission and tracking
- Attendance monitoring
- Grade and transcript viewing
- Fee payment status
- Library book management

### Faculty Portal
- Course assignment management
- Student grading and evaluation
- Attendance marking
- Research work tracking
- Leave management
- Performance evaluations

### Admin Panel
- User and role management
- System configuration
- Report generation
- Announcement management
- Policy and procedure management
- Grievance handling

### Back-office Operations
- Financial management and accounting
- HR and payroll processing
- Library management
- Hostel allocation
- Inventory tracking
- Fee collection

## 🛠️ API Endpoints

### Authentication
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `GET /api/auth/profile/` - Get user profile
- `POST /api/auth/change-password/` - Change password

### Students
- `GET /api/students/` - List students
- `GET /api/students/dashboard/{id}/` - Student dashboard
- `GET /api/students/courses/` - List courses
- `POST /api/students/attendance/mark/` - Mark attendance

### Faculty
- `GET /api/faculty/` - List faculty
- `GET /api/faculty/assignments/` - Course assignments
- `POST /api/faculty/leaves/` - Submit leave request

### Exams
- `GET /api/exams/` - List exams
- `GET /api/exams/results/` - Exam results
- `POST /api/exams/register/` - Register for exam

### Admissions
- `GET /api/admissions/cycles/` - Admission cycles
- `POST /api/admissions/applications/` - Submit application
- `POST /api/admissions/documents/` - Upload documents

## 🗄️ Database Schema

### Key Models
- **User** - Custom user model with role-based access
- **Student** - Student information and academic data
- **Faculty** - Faculty information and assignments
- **Course** - Course catalog and prerequisites
- **Enrollment** - Student course enrollments
- **Exam** - Examination management
- **Application** - Admission applications

## 🔒 Security Features
- JWT-based authentication
- Role-based access control
- API rate limiting
- Input validation and sanitization
- Audit logging
- CORS protection

## 📱 Responsive Design
- Mobile-first responsive design
- Clean and intuitive user interface
- Role-based navigation
- Dark/light theme support (configurable)

## 📈 Analytics & Reporting
- Student performance analytics
- Faculty workload reports
- Financial reports
- Attendance analytics
- Admission statistics
- Custom report generation

## 🔧 Development

### Running Tests
```bash
# Backend tests
python manage.py test

# Frontend tests
cd frontend_react
npm test
```

### Code Quality
- ESLint and Prettier for frontend
- Black and isort for backend
- Type checking with TypeScript

## 🚀 Production Deployment

### Database Configuration (MySQL)
1. Install MySQL server
2. Create database: `university_erp_db`
3. Update `settings.py` database configuration
4. Install additional requirements: `pip install cryptography`

### Environment Variables
Create `.env` file:
```
SECRET_KEY=your-secret-key
DEBUG=False
DATABASE_URL=mysql://user:pass@localhost/university_erp_db
ALLOWED_HOSTS=your-domain.com
```

### Docker Deployment (Optional)
```dockerfile
# Dockerfile example for production deployment
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "university_erp.wsgi:application"]
```

## 📞 Support & Documentation
- Admin Panel: http://localhost:8000/admin/
- API Documentation: http://localhost:8000/api/
- Frontend: http://localhost:3000/

## 🎯 Next Steps
1. Configure MySQL database for production
2. Set up email notifications
3. Implement payment gateway integration
4. Add AI-powered analytics
5. Mobile app development
6. Integration with external systems

## 📄 License
This University ERP system is built for educational purposes and can be customized according to institutional needs.

---

**Built with ❤️ using Django + React + TailwindCSS**
