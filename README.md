# Django Expense Tracker API

A RESTful API for tracking expenses and incomes built with Django and Django REST Framework.  
Includes user authentication with JWT, CRUD operations on transactions, tax calculations, and permissions.

---

## Features

- User registration and login with JSON Web Tokens (JWT) using SimpleJWT
- Create, read, update, and delete expenses and incomes
- Tax calculation with flat or percentage tax types
- Permissions so users can only access their own transactions; superusers can access all
- Pagination support for listing transactions
- Automated tests for authentication and expense endpoints
- Sample data creation management command

---

## Tech Stack

- Python 3.x  
- Django 4.x  
- Django REST Framework  
- djangorestframework-simplejwt  
- SQLite (default database)

---

## Getting Started

### Prerequisites

- Python 3.8+  
- pip (Python package manager)  

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/django-expense-tracker.git
   cd django-expense-tracker
  
2. **Install dependencies**
   ```
   pip install -r requirements.txt
3. **Apply database migrations**
   ```
   python manage.py migrate

4. **Create a superuser**
   ```
   python manage.py createsuperuser
5. **Run the development server**
   ```
   python manage.py runserver
   
