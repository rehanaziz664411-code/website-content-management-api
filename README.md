# Website Content Management API

A production-ready RESTful API built with FastAPI for dynamically managing website content, including:

* Header Management
* Hero Section Management
* FAQ Management
* Footer Management

The project follows a modular architecture using FastAPI, SQLAlchemy ORM, Pydantic validation, and API Key Authentication, making it suitable for real-world content management systems (CMS), admin dashboards, and portfolio projects.

---

# Features

✅ FastAPI REST API

✅ SQLAlchemy ORM

✅ SQLite Database

✅ API Key Authentication

✅ Pydantic Request/Response Validation

✅ Modular Router Architecture

✅ Swagger API Documentation

✅ ReDoc Documentation

✅ Singleton Configuration Models

✅ Dynamic Content Management

✅ Production-Ready Project Structure

---

# Project Architecture

```text
website-content-management-api/
│
├── requirements.txt
├── .env.example
│
└── app/
    ├── __init__.py
    ├── main.py
    ├── database.py
    ├── models.py
    ├── schemas.py
    ├── auth.py
    │
    └── routers/
        ├── __init__.py
        ├── header.py
        ├── hero.py
        ├── faq.py
        └── footer.py
```

---

# Technologies Used

| Technology    | Purpose               |
| ------------- | --------------------- |
| Python 3      | Programming Language  |
| FastAPI       | REST API Framework    |
| SQLAlchemy    | ORM                   |
| SQLite        | Database              |
| Pydantic      | Data Validation       |
| Uvicorn       | ASGI Server           |
| Python-Dotenv | Environment Variables |

---

# API Modules

## 1. Header API

Manages:

* Website Logo
* Navigation Menus
* Header Action Buttons

Endpoints:

```http
GET     /api/header
PUT     /api/header/logo
POST    /api/header/nav-menu
PUT     /api/header/nav-menu/{id}
DELETE  /api/header/nav-menu/{id}
POST    /api/header/action-buttons
PUT     /api/header/action-buttons/{id}
DELETE  /api/header/action-buttons/{id}
```

---

## 2. Hero Section API

Manages:

* Hero Title
* Subtitle
* Banner Image
* CTA Buttons

Endpoints:

```http
GET     /api/hero
PUT     /api/hero
POST    /api/hero/cta-buttons
PUT     /api/hero/cta-buttons/{id}
DELETE  /api/hero/cta-buttons/{id}
```

---

## 3. FAQ API

Manages:

* Frequently Asked Questions
* Ordering
* Active Status

Endpoints:

```http
GET     /api/faqs
GET     /api/faqs/{id}
POST    /api/faqs
PUT     /api/faqs/{id}
DELETE  /api/faqs/{id}
```

---

## 4. Footer API

Manages:

* Contact Information
* Footer Links
* Social Media Links
* Copyright Information

Endpoints:

```http
GET     /api/footer
PUT     /api/footer/contact
POST    /api/footer/links
PUT     /api/footer/links/{id}
DELETE  /api/footer/links/{id}
POST    /api/footer/social-links
PUT     /api/footer/social-links/{id}
DELETE  /api/footer/social-links/{id}
```

---

# Authentication

The API uses API Key Authentication for all administrative operations.

Protected endpoints require:

```http
X-API-Key: your-secret-api-key
```

Public GET endpoints do not require authentication.

---

# Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/website-content-management-api.git
cd website-content-management-api
```

## Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a .env file:

```env
ADMIN_API_KEY=your-super-secret-api-key
```

---

# Run Application

```bash
uvicorn app.main:app --reload
```

Application:

```text
http://127.0.0.1:8000
```

Swagger Documentation:

```text
http://127.0.0.1:8000/docs
```

ReDoc Documentation:

```text
http://127.0.0.1:8000/redoc
```

---

# Design Principles

* Modular Architecture
* Separation of Concerns
* Dependency Injection
* Schema Validation
* Secure Administrative APIs
* Scalable Project Structure
* Clean Code Practices

---

# Future Improvements

* JWT Authentication
* PostgreSQL Support
* Docker Deployment
* Unit Testing
* CI/CD Pipeline
* File Upload Support
* Redis Caching
* Role-Based Access Control (RBAC)
* Admin Dashboard Integration

---

# Use Cases

This project can be used as:

* Website Content Management System (CMS)
* Portfolio Project
* Internship Project
* Backend Development Demonstration
* Admin Dashboard Backend
* Startup Landing Page Management System

---

# Author

Rehan Aziz

AI Engineer | Machine Learning Engineer | Backend Developer | FastAPI Developer

GitHub: https://github.com/yourusername

---

# License

This project is licensed under the MIT License.
