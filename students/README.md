# Students App Documentation

## Overview
This document explains the creation and implementation of the `students` Django application within our Django practice project.

## What We Created

### 1. Django App Creation
We created a new Django application called `students` using the Django management command:

```bash
python manage.py startapp students
```

This command generated the following directory structure:
```
students/
├── __init__.py
├── admin.py
├── apps.py
├── migrations/
│   └── __init__.py
├── models.py
├── tests.py
└── views.py
```

### 2. App Registration
We registered the `students` app in the Django project by adding it to `INSTALLED_APPS` in `practice_project/settings.py`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',
    'students',  # ← Added this line
]
```

### 3. Student Model Creation
We created a `Student` model in `students/models.py` with the following fields:

```python
from django.db import models

class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.nickname})"
```

#### Model Fields Explanation:
- **first_name**: CharField with maximum 100 characters for the student's first name
- **last_name**: CharField with maximum 100 characters for the student's last name  
- **nickname**: CharField with maximum 50 characters for the student's nickname
- **__str__ method**: Returns a readable string representation of the student

### 4. Database Migrations

#### Creating Migrations
We generated a migration file for our new model:

```bash
python manage.py makemigrations students
```

This created `students/migrations/0001_initial.py` which contains the database schema for our Student model.

#### Applying Migrations
We applied the migrations to create the actual database table:

```bash
python manage.py migrate
```

This created the `students_student` table in our PostgreSQL database with the following structure:

| Column     | Type         | Description                    |
|------------|--------------|--------------------------------|
| id         | INTEGER      | Auto-generated primary key     |
| first_name | VARCHAR(100) | Student's first name           |
| last_name  | VARCHAR(100) | Student's last name            |
| nickname   | VARCHAR(50)  | Student's nickname             |

### 5. Django ORM Testing

#### Creating a Student via Django Shell
We tested our model by creating a student record using Django's ORM:

```python
# In Django shell (python manage.py shell)
from students.models import Student

# Create a new student
student = Student.objects.create(
    first_name="John",
    last_name="Doe", 
    nickname="JD"
)

# Verify creation
print(f"Created student: {student}")
print(f"Student ID: {student.id}")
```

#### Verifying in PostgreSQL
We confirmed the student was created by querying the database directly:

```sql
-- In PostgreSQL
SELECT * FROM students_student;
```

**Result:**
```
 id | first_name | last_name | nickname 
----+------------+-----------+----------
  1 | John       | Doe       | JD
(1 row)
```

## Files Modified

### 1. `practice_project/settings.py`
- **Change**: Added `'students'` to `INSTALLED_APPS`
- **Purpose**: Register the new app with Django

### 2. `students/models.py`
- **Change**: Created `Student` model with three fields
- **Purpose**: Define the database structure for student data

### 3. Database Schema
- **Change**: New table `students_student` created in PostgreSQL
- **Purpose**: Store student records in the database

## Commands Executed

| Command | Purpose |
|---------|---------|
| `python manage.py startapp students` | Create new Django app |
| `python manage.py makemigrations students` | Generate migration files |
| `python manage.py migrate` | Apply migrations to database |
| `python manage.py shell` | Open Django interactive shell |
| `sudo -u postgres psql -d django_practice -c "SELECT * FROM students_student;"` | Query database directly |

## Learning Outcomes

Through this exercise, we demonstrated:

1. **Django App Architecture**: How to create modular applications within a Django project
2. **Model Definition**: Defining database models using Django's ORM
3. **Database Migrations**: Managing database schema changes through Django migrations
4. **ORM Usage**: Creating and querying database records using Django's Object-Relational Mapping
5. **Database Integration**: How Django models translate to actual database tables
6. **Development Workflow**: The complete cycle from model creation to database verification

## Next Steps

Potential enhancements for the students app:
- Add more fields (email, date_of_birth, enrollment_date)
- Create admin interface registration
- Add model validation
- Create views and templates for web interface
- Add relationships to other models (courses, grades, etc.)

---

*Created as part of Django learning practice project - September 16, 2025*
