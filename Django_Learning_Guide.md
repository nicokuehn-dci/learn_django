# Django Learning Guide

## Table of Contents

1. [Introduction to Django](#introduction-to-django)
2. [Setting Up Django](#setting-up-django)
3. [Django Project Structure](#django-project-structure)
4. [Django Apps](#django-apps)
5. [Models and Databases](#models-and-databases)
6. [Django ORM](#django-orm)
7. [Views and URL Patterns](#views-and-url-patterns)
8. [Templates](#templates)
9. [Forms](#forms)
10. [Admin Interface](#admin-interface)
11. [Authentication and Authorization](#authentication-and-authorization)
12. [Static and Media Files](#static-and-media-files)
13. [Middleware](#middleware)
14. [Testing in Django](#testing-in-django)
15. [Deployment](#deployment)
16. [Best Practices](#best-practices)
17. [Useful Resources](#useful-resources)
18. [**Hands-On Practice Project**](#hands-on-practice-project) 🚀

## 🚀 Hands-On Practice Project

**We built a complete Project Management System from scratch!**

This section documents our step-by-step journey creating a real Django application with PostgreSQL database, complete models, admin interface, and migrations.

### 📋 Project Overview

**Project Name**: Django Practice Project  
**App Name**: main  
**Database**: PostgreSQL  
**Models**: Project, Stage, Task (with relationships)  
**Features**: Complete admin interface, user authentication, database migrations

### 🎯 What We Built

A project management system with:
- **Projects**: Container for organizing work
- **Stages**: Workflow steps (TO_DO, DONE, FINISHED) 
- **Tasks**: Individual work items with assignments and tracking
- **User System**: Built-in Django authentication
- **Admin Panel**: Full CRUD operations for all models

### 🛠️ Step 1: Project Setup

#### Creating the Project Structure
```bash
# Navigate to workspace
cd "/home/nico-kuehn-dci/Desktop/DCI Learning./DCI Learning/django_practice"

# Create virtual environment
python -m venv practice_venv

# Activate virtual environment
source practice_venv/bin/activate

# Install Django
pip install django psycopg2-binary

# Create Django project
django-admin startproject practice_project .

# Create Django app
python manage.py startapp main
```

#### Project Structure Created
```
django_practice/
├── practice_venv/          # Virtual environment
├── practice_project/       # Main project settings
│   ├── settings.py        # Configuration
│   ├── urls.py           # URL routing
│   └── wsgi.py           # WSGI config
├── main/                  # Our app
│   ├── models.py         # Database models
│   ├── admin.py          # Admin configuration
│   ├── views.py          # View controllers
│   └── migrations/       # Database migrations
└── manage.py             # Django management commands
```

### 🗄️ Step 2: Database Configuration

#### PostgreSQL Setup
```python
# practice_project/settings.py
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "django_practice",
        "USER": "postgres", 
        "PASSWORD": "postgres",
        "HOST": "127.0.0.1",
        "PORT": "5432",
    }
}

# Add our app to INSTALLED_APPS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',  # ← Our app added here
]
```

#### Database Creation
```bash
# Create PostgreSQL database
sudo -u postgres createdb django_practice

# Run initial migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
# Username: admin
# Password: postgres
```

### 📊 Step 3: Creating Models

#### Our Database Schema
Based on the diagram analysis, we created three interconnected models:

```python
# main/models.py
from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Stage(models.Model):
    name = models.CharField(max_length=50, unique=True)   
    order_no = models.PositiveIntegerField()

    class Meta:
        ordering = ['order_no']

    def __str__(self):
        return self.name

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    # Relationships
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    assignee = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='tasks')
    stage = models.ForeignKey(Stage, on_delete=models.RESTRICT, related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
```

#### 🔗 Model Relationships Explained

- **Project ↔ Task**: One-to-Many (One project has many tasks)
- **Stage ↔ Task**: One-to-Many (One stage can have many tasks)  
- **User ↔ Task**: One-to-Many (One user can be assigned to many tasks)
- **Foreign Key Options**:
  - `CASCADE`: Delete tasks when project is deleted
  - `SET_NULL`: Keep task but remove assignee when user is deleted
  - `RESTRICT`: Prevent stage deletion if tasks exist

### 🔄 Step 4: Database Migrations

#### Creating and Applying Migrations
```bash
# Create migrations for model changes
python manage.py makemigrations

# Output:
# Migrations for 'main':
#   main/migrations/0001_initial.py
#     + Create model Project
#     + Create model Stage
#   main/migrations/0002_task.py  
#     + Create model Task

# Apply migrations to database
python manage.py migrate

# Output:
# Operations to perform:
#   Apply all migrations: admin, auth, contenttypes, main, sessions
# Running migrations:
#   Applying main.0001_initial... OK
#   Applying main.0002_task... OK
```

#### 📋 Understanding Migration Files

**Migration 0001_initial.py** - Creates Project and Stage tables:
```python
operations = [
    migrations.CreateModel(
        name='Project',
        fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True)),
            ('name', models.CharField(max_length=255)),
            ('description', models.TextField(blank=True)),
            ('created_at', models.DateTimeField(auto_now_add=True)),
        ],
    ),
    # ... Stage model creation
]
```

**Migration 0002_task.py** - Creates Task table with relationships:
```python
operations = [
    migrations.CreateModel(
        name='Task',
        fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True)),
            ('title', models.CharField(max_length=255)),
            ('description', models.TextField(blank=True)),
            ('created_at', models.DateTimeField(auto_now_add=True)),
            ('updated_at', models.DateTimeField(auto_now=True)),
            ('assignee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tasks', to=settings.AUTH_USER_MODEL)),
            ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='main.project')),
            ('stage', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='tasks', to='main.stage')),
        ],
    ),
]
```

### 🗃️ Step 5: Generated SQL (PostgreSQL)

#### Viewing Generated SQL
```bash
# See SQL that Django generates for migrations
python manage.py sqlmigrate main 0001
python manage.py sqlmigrate main 0002
```

#### SQL Output for Migration 0001:
```sql
BEGIN;
-- Create model Project
CREATE TABLE "main_project" (
    "id" bigint NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY, 
    "name" varchar(255) NOT NULL, 
    "description" text NOT NULL, 
    "created_at" timestamp with time zone NOT NULL
);

-- Create model Stage  
CREATE TABLE "main_stage" (
    "id" bigint NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY, 
    "name" varchar(50) NOT NULL UNIQUE, 
    "order_no" integer NOT NULL CHECK ("order_no" >= 0)
);
CREATE INDEX "main_stage_name_341fdc32_like" ON "main_stage" ("name" varchar_pattern_ops);
COMMIT;
```

#### SQL Output for Migration 0002:
```sql
BEGIN;
-- Create model Task
CREATE TABLE "main_task" (
    "id" bigint NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY, 
    "title" varchar(255) NOT NULL, 
    "description" text NOT NULL, 
    "created_at" timestamp with time zone NOT NULL, 
    "updated_at" timestamp with time zone NOT NULL, 
    "assignee_id" integer NULL, 
    "project_id" bigint NOT NULL, 
    "stage_id" bigint NOT NULL
);

-- Foreign Key Constraints
ALTER TABLE "main_task" ADD CONSTRAINT "main_task_assignee_id_872aa96a_fk_auth_user_id" 
    FOREIGN KEY ("assignee_id") REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "main_task" ADD CONSTRAINT "main_task_project_id_45272a98_fk_main_project_id" 
    FOREIGN KEY ("project_id") REFERENCES "main_project" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "main_task" ADD CONSTRAINT "main_task_stage_id_ab22ee17_fk_main_stage_id" 
    FOREIGN KEY ("stage_id") REFERENCES "main_stage" ("id") DEFERRABLE INITIALLY DEFERRED;

-- Performance Indexes
CREATE INDEX "main_task_assignee_id_872aa96a" ON "main_task" ("assignee_id");
CREATE INDEX "main_task_project_id_45272a98" ON "main_task" ("project_id");
CREATE INDEX "main_task_stage_id_ab22ee17" ON "main_task" ("stage_id");
COMMIT;
```

#### 🎯 Key PostgreSQL Features Used:
- **IDENTITY columns**: Auto-incrementing primary keys
- **UNIQUE constraints**: Ensuring stage names are unique
- **CHECK constraints**: Validating positive integers (order_no >= 0)
- **Foreign key constraints**: Maintaining referential integrity
- **Indexes**: Optimizing query performance on foreign keys
- **DEFERRABLE constraints**: Better transaction handling

### 🎛️ Step 6: Admin Interface Setup

#### Configuring Admin Panel
```python
# main/admin.py
from django.contrib import admin
from .models import Project, Stage, Task

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']

@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ['name', 'order_no']
    list_editable = ['order_no']
    ordering = ['order_no']

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'project', 'stage', 'assignee', 'created_at']
    list_filter = ['stage', 'project', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['stage']
```

#### Admin Features Created:
- **Project Management**: List view with search and date filtering
- **Stage Management**: Inline editing of order numbers
- **Task Management**: Comprehensive filtering and stage updates
- **User Management**: Built-in Django user administration

### 🚀 Step 7: Running the Application

#### Starting the Development Server
```bash
# Activate virtual environment
source practice_venv/bin/activate

# Start Django development server
python manage.py runserver 8001

# Output:
# Watching for file changes with StatReloader
# Performing system checks...
# System check identified no issues (0 silenced).
# September 16, 2025 - 08:27:39
# Django version 5.2.6, using settings 'practice_project.settings'
# Starting development server at http://127.0.0.1:8001/
# Quit the server with CONTROL-C.
```

#### 🌐 Access Points:
- **Main Site**: http://127.0.0.1:8001/
- **Admin Panel**: http://127.0.0.1:8001/admin/
- **Login Credentials**: 
  - Username: `admin`
  - Password: `postgres`

### 📋 Step 8: Essential Django Commands Used

#### Project Management Commands
```bash
# Virtual Environment
python -m venv practice_venv           # Create virtual environment
source practice_venv/bin/activate      # Activate (Linux/Mac)

# Django Project Setup  
django-admin startproject practice_project .  # Create project
python manage.py startapp main                # Create app

# Database Operations
python manage.py makemigrations        # Create migration files
python manage.py migrate               # Apply migrations to database
python manage.py sqlmigrate main 0001  # View SQL for specific migration
python manage.py showmigrations        # Show migration status

# User Management
python manage.py createsuperuser       # Create admin user
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'postgres')" | python manage.py shell

# Development Server
python manage.py runserver 8001        # Start development server on port 8001

# Database Inspection
python manage.py shell                 # Interactive Django shell
python manage.py dbshell              # Database command line
```

#### 🔧 Migration Workflow
```bash
# Standard workflow for model changes:
1. Edit models.py                      # Make changes to models
2. python manage.py makemigrations     # Create migration files  
3. python manage.py migrate            # Apply to database
4. python manage.py runserver          # Test changes
```

### 🎓 Key Learning Points

#### 1. **Django Project Structure**
- **Project** vs **App**: Project contains multiple apps
- **Settings**: Central configuration in `settings.py`
- **URLs**: Routing system for web requests
- **Apps**: Modular components with specific functionality

#### 2. **Model Design Principles**
- **Models represent database tables** as Python classes
- **Field types** define data types and constraints
- **Relationships** connect models (ForeignKey, ManyToMany, OneToOne)
- **Meta options** control model behavior and database features

#### 3. **Database Migrations**
- **Version control for database schema** changes
- **Automatic SQL generation** from Python models
- **Reversible operations** for safe deployment
- **Dependency tracking** between migrations

#### 4. **Admin Interface Benefits**
- **Instant CRUD operations** without custom views
- **User-friendly interface** for non-technical users
- **Customizable displays** and filtering options
- **Built-in authentication** and permissions

#### 5. **PostgreSQL Integration**
- **Production-ready database** with advanced features
- **ACID compliance** for data integrity
- **Advanced data types** and indexing
- **Scalability** for large applications

#### 6. **Development Workflow**
- **Virtual environments** for dependency isolation
- **Iterative development** with automatic reloading
- **Version control** through migrations
- **Testing environment** separate from production

### 🔧 Troubleshooting & Solutions

#### Common Issues We Encountered:

**1. PostgreSQL Connection Errors**
```bash
# Problem: psycopg2.OperationalError: database "django_practice" does not exist
# Solution: Create the database first
sudo -u postgres createdb django_practice
```

**2. Virtual Environment Issues**
```bash
# Problem: Command 'python' not found
# Solution: Always activate virtual environment first
source practice_venv/bin/activate
```

**3. Migration Not Detected** 
```bash
# Problem: "No changes detected" when models were changed
# Solution: Check file syntax and force migration creation
python manage.py makemigrations main --empty
```

**4. Port Already in Use**
```bash
# Problem: "That port is already in use"
# Solution: Use different port or kill existing process
python manage.py runserver 8001  # Use different port
```

**5. Admin User Creation**
```bash
# Problem: Need admin access but forgot to create superuser
# Solution: Create via Django shell
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'postgres')" | python manage.py shell
```

### 🚀 Next Steps & Extensions

#### Immediate Improvements:
1. **Add Views & Templates**: Create public-facing pages
2. **URL Configuration**: Set up proper routing
3. **Forms**: Add custom forms for data entry  
4. **Static Files**: Add CSS and JavaScript
5. **Testing**: Write unit tests for models and views

#### Advanced Features:
1. **REST API**: Use Django REST Framework
2. **User Authentication**: Custom login/logout pages
3. **Permissions**: Role-based access control
4. **File Uploads**: Handle media files
5. **Email Integration**: Send notifications
6. **Caching**: Improve performance
7. **Docker**: Containerize the application
8. **Deployment**: Deploy to production server

#### Learning Progression:
1. **Master Django Basics** ✅ (We did this!)
2. **Frontend Integration**: HTML, CSS, JavaScript
3. **API Development**: RESTful services
4. **Testing Strategies**: Unit, integration, and functional tests
5. **Performance Optimization**: Database queries and caching
6. **Security Best Practices**: Authentication and authorization
7. **Deployment**: Production server setup and monitoring

### 📊 Project Summary

#### ✅ What We Accomplished:

| Component | Status | Description |
|-----------|--------|-------------|
| **Project Setup** | ✅ Complete | Virtual environment, Django installation, project creation |
| **Database** | ✅ Complete | PostgreSQL configuration and connection |
| **Models** | ✅ Complete | Project, Stage, Task models with relationships |
| **Migrations** | ✅ Complete | Database schema creation and version control |
| **Admin** | ✅ Complete | Full CRUD interface for all models |
| **Authentication** | ✅ Complete | Superuser creation and login system |
| **Server** | ✅ Complete | Development server running on port 8001 |

#### 📈 Skills Developed:
- ✅ Django project structure and configuration
- ✅ Model design and database relationships  
- ✅ PostgreSQL integration and setup
- ✅ Migration system understanding
- ✅ Admin interface customization
- ✅ Command-line Django management
- ✅ Virtual environment management
- ✅ Troubleshooting common Django issues

#### 🎯 Real-World Application:
This project demonstrates core concepts used in professional Django development:
- **Scalable architecture** with proper app separation
- **Database best practices** with PostgreSQL and migrations  
- **User management** with Django's built-in auth system
- **Admin interface** for content management
- **Development workflow** with virtual environments and version control

**Total Development Time**: ~2 hours  
**Lines of Code**: ~100 lines of Python  
**Database Tables**: 6 tables (3 custom + 3 Django built-in)  
**Features**: Complete project management system with admin interface

🎉 **Congratulations! You've built a complete Django application from scratch!**

## Introduction to Django

Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. Built by experienced developers, it takes care of much of the hassle of web development, so you can focus on writing your app without needing to reinvent the wheel.

### Key Features

- **Batteries Included**: Django comes with many built-in features like authentication, URL routing, templating, ORM, and database schema migrations.
- **Secure**: Django helps developers avoid many common security mistakes like SQL injection, cross-site scripting, cross-site request forgery, and clickjacking.
- **Scalable**: Django can scale to meet the heaviest traffic demands.
- **Versatile**: Django can be used to build almost any type of website - from content management systems and wikis to social networks and news sites.
- **DRY Principle**: Django follows the "Don't Repeat Yourself" principle, encouraging reusability of code.

### Django's Architecture

Django follows the Model-View-Template (MVT) architectural pattern:

- **Model**: Defines your data structure and handles database operations.
- **View**: Controls what the user sees, retrieving data from models and rendering templates.
- **Template**: Defines how the data is presented to the user (HTML).

## Setting Up Django

### Installation

Django requires Python to be installed. To install Django:

```bash
pip install django

```

To check your Django version:

```bash
python -m django --version

```

### Creating a Project

To create a new Django project:

```bash
django-admin startproject projectname

```

This creates a directory structure:

```sh
projectname/
    manage.py
    projectname/
        __init__.py
        settings.py
        urls.py
        asgi.py
        wsgi.py

```

### Running the Development Server

Navigate to your project directory and run:

```bash
python manage.py runserver

```

Access your website at http://127.0.0.1:8000/

## Django Project Structure

### manage.py

A command-line utility that lets you interact with your Django project.

### __init__.py

An empty file that tells Python that this directory should be considered a Python package.

### settings.py

Contains all the configuration for your Django project, including database settings, installed apps, middleware, etc.

### urls.py

The URL declarations for this Django project; a "table of contents" for your Django-powered site.

### asgi.py

An entry-point for ASGI-compatible web servers to serve your project.

### wsgi.py

An entry-point for WSGI-compatible web servers to serve your project.

## Django Apps

Django projects are made up of apps - modular components that handle specific functionality.

### Creating an App

```bash
python manage.py startapp appname

```

This creates a directory:

```sh
appname/
    __init__.py
    admin.py
    apps.py
    migrations/
        __init__.py
    models.py
    tests.py
    views.py

```

### Registering an App

Add your app to `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'appname',  # Add your app here
]

```

## Models and Databases

Models define your database schema and are Python classes that subclass `django.db.models.Model`.

### Example Model

```python
from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    
    def __str__(self):
        return self.name
        
class Book(models.Model):
    title = models.CharField(max_length=200)
    publication_date = models.DateField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title

```

### Field Types

Django provides many field types:

- `CharField` - String field
- `TextField` - Large text
- `IntegerField` - Integer
- `FloatField` - Floating-point number
- `BooleanField` - True/False
- `DateField` - Date
- `TimeField` - Time
- `DateTimeField` - Date and time
- `EmailField` - Email address
- `FileField` - File upload
- `ImageField` - Image upload
- `ForeignKey` - Many-to-one relationship
- `ManyToManyField` - Many-to-many relationship
- `OneToOneField` - One-to-one relationship

### Migrations

Migrations are Django's way of propagating changes you make to your models into your database schema.

To create migrations:

```bash
python manage.py makemigrations

```

To apply migrations:

```bash
python manage.py migrate

```

## Django ORM

Django's Object-Relational Mapper (ORM) lets you interact with your database in a Pythonic way.

### Creating Objects

```python
author = Author(name='J.K. Rowling', email='jk@example.com')
author.save()

# Alternative way:
Author.objects.create(name='J.K. Rowling', email='jk@example.com')

```

### Querying Objects

```python
# Get all authors
authors = Author.objects.all()

# Filter authors
rowling = Author.objects.filter(name='J.K. Rowling')

# Get a single object
try:
    author = Author.objects.get(id=1)
except Author.DoesNotExist:
    # Handle not found
    pass

# Order objects
ordered_authors = Author.objects.order_by('name')

# Complex queries
from django.db.models import Q
complex_query = Author.objects.filter(
    Q(name__startswith='J') | Q(email__contains='example.com')
)

```

### Updating Objects

```python
author = Author.objects.get(id=1)
author.name = 'New Name'
author.save()

# Update multiple records
Author.objects.filter(name='J.K. Rowling').update(email='new_email@example.com')

```

### Deleting Objects

```python
author = Author.objects.get(id=1)
author.delete()

# Delete multiple records
Author.objects.filter(name='J.K. Rowling').delete()

```

### Related Objects

```python
# Access related objects
author = Author.objects.get(id=1)
books = author.book_set.all()  # All books by this author

# Create related objects
book = author.book_set.create(title='Harry Potter', publication_date='1997-06-26')

```

## Views and URL Patterns

Views handle HTTP requests and return HTTP responses. URL patterns map URLs to views.

### Function-Based Views

```python
# views.py
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Book

def home(request):
    return HttpResponse('Welcome to my site!')

def book_list(request):
    books = Book.objects.all()
    return render(request, 'books/book_list.html', {'books': books})

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'books/book_detail.html', {'book': book})

```

### Class-Based Views

```python
# views.py
from django.views import generic
from .models import Book

class BookListView(generic.ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'

class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'

```

### URL Patterns

```python
# urls.py (project level)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('books/', include('books.urls')),
]

# urls.py (app level)
from django.urls import path
from . import views

app_name = 'books'  # For namespacing

urlpatterns = [
    path('', views.BookListView.as_view(), name='list'),
    path('<int:pk>/', views.BookDetailView.as_view(), name='detail'),
    # For function-based views:
    # path('', views.book_list, name='list'),
    # path('<int:book_id>/', views.book_detail, name='detail'),
]

```

## Templates

Templates are HTML files with Django template language that can dynamically display data.

### Template Structure

```sh
projectname/
    templates/
        base.html
        appname/
            template.html

```

Add your templates directory to `settings.py`:

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        # ...
    },
]

```

### Template Inheritance

```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}My Site{% endblock %}</title>
</head>
<body>
    <header>My Website</header>
    <main>
        {% block content %}
        {% endblock %}
    </main>
    <footer>Copyright 2023</footer>
</body>
</html>

<!-- templates/books/book_list.html -->
{% extends 'base.html' %}

{% block title %}Book List{% endblock %}

{% block content %}
    <h1>Books</h1>
    <ul>
        {% for book in books %}
            <li><a href="{% url 'books:detail' book.id %}">{{ book.title }}</a></li>
        {% empty %}
            <li>No books available.</li>
        {% endfor %}
    </ul>
{% endblock %}

```

### Template Tags and Filters

```html
<!-- Variables -->
{{ variable }}

<!-- If statement -->
{% if user.is_authenticated %}
    Hello, {{ user.username }}!
{% else %}
    Please log in.
{% endif %}

<!-- For loop -->
{% for item in items %}
    {{ item }}
{% endfor %}

<!-- Filters -->
{{ name|lower }}
{{ text|truncatewords:30 }}
{{ date|date:"Y-m-d" }}

<!-- URL Tag -->
<a href="{% url 'books:detail' book.id %}">{{ book.title }}</a>

<!-- Static Files -->
{% load static %}
<img src="{% static 'images/logo.png' %}" alt="Logo">

<!-- CSRF Token -->
<form method="post">
    {% csrf_token %}
    <!-- form fields -->
</form>

```

## Forms

Django provides a powerful forms library for handling user input.

### Form Definition

```python
# forms.py
from django import forms
from .models import Book

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'publication_date', 'author']
        # or fields = '__all__' for all fields

```

### Using Forms in Views

```python
# views.py
from django.shortcuts import render, redirect
from .forms import ContactForm, BookForm

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the data
            name = form.cleaned_data['name']
            # ...
            return redirect('thank_you')
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})

def create_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('books:list')
    else:
        form = BookForm()
    
    return render(request, 'books/create_book.html', {'form': form})

```

### Rendering Forms in Templates

```html
<form method="post">
    {% csrf_token %}
    
    <!-- Render the entire form -->
    {{ form.as_p }}
    <!-- Other options: form.as_table, form.as_ul -->
    
    <!-- Or render fields individually -->
    <div>
        <label for="{{ form.name.id_for_label }}">Name:</label>
        {{ form.name }}
        {{ form.name.errors }}
    </div>
    
    <button type="submit">Submit</button>
</form>

```

## Admin Interface

Django comes with a powerful admin interface that's automatically generated based on your models.

### Registering Models

```python
# admin.py
from django.contrib import admin
from .models import Author, Book

admin.site.register(Author)
admin.site.register(Book)

```

### Customizing Admin

```python
# admin.py
from django.contrib import admin
from .models import Author, Book

class BookInline(admin.TabularInline):
    model = Book
    extra = 1  # Number of empty forms to display

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name', 'email')
    inlines = [BookInline]

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'publication_date', 'author')
    list_filter = ('publication_date', 'author')
    search_fields = ('title',)
    date_hierarchy = 'publication_date'

```

### Creating a Superuser

```bash
python manage.py createsuperuser

```

## Authentication and Authorization

Django comes with a built-in authentication system.

### User Authentication Views

```python
# urls.py (project level)
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    # ...
]

```

### Custom User Model

```python
# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    
# settings.py
AUTH_USER_MODEL = 'yourapp.CustomUser'

```

### Permissions

```python
# Checking permissions
if request.user.has_perm('app.add_model'):
    # User can add model
    pass

# Using decorators
from django.contrib.auth.decorators import login_required, permission_required

@login_required
def profile(request):
    return render(request, 'profile.html')

@permission_required('app.add_model')
def add_model(request):
    # Add model logic
    pass

# For class-based views
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class ProtectedView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'app.view_model'
    # ...

```

## Static and Media Files

Django handles static files (CSS, JavaScript, images) and media files (user-uploaded content).

### Static Files

```python
# settings.py
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # For collectstatic

```

In templates:

```html
{% load static %}
<link rel="stylesheet" href="{% static 'css/style.css' %}">
<script src="{% static 'js/script.js' %}"></script>
<img src="{% static 'images/logo.png' %}" alt="Logo">

```

### Media Files

```python
# settings.py
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# urls.py (project level, for development)
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

```

In models:

```python
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/')

```

## Middleware

Middleware are hooks that process requests and responses globally.

### Built-in Middleware

Django includes several middleware:

```python
# settings.py
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

```

### Custom Middleware

```python
# middleware.py
class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code executed for each request before the view is called
        response = self.get_response(request)
        # Code executed for each response after the view is called
        return response

```

Add to `settings.py`:

```python
MIDDLEWARE = [
    # ...
    'yourapp.middleware.SimpleMiddleware',
]

```

## Testing in Django

Django provides tools for testing your applications.

### Testing Models

```python
# tests.py
from django.test import TestCase
from .models import Author, Book

class AuthorModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name='Test Author', email='test@example.com')

    def test_author_creation(self):
        self.assertEqual(self.author.name, 'Test Author')
        self.assertEqual(self.author.email, 'test@example.com')

```

### Testing Views

```python
# tests.py
from django.test import TestCase, Client
from django.urls import reverse
from .models import Book, Author

class BookViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.author = Author.objects.create(name='Test Author', email='test@example.com')
        self.book = Book.objects.create(
            title='Test Book',
            publication_date='2023-01-01',
            author=self.author
        )
        self.list_url = reverse('books:list')
        self.detail_url = reverse('books:detail', args=[self.book.id])

    def test_book_list_view(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Book')
        
    def test_book_detail_view(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Book')

```

### Running Tests

```bash
python manage.py test
python manage.py test app_name
python manage.py test app_name.tests.TestClassName

```

## Deployment

Deploying Django applications involves several steps:

### Preparation

1. Update `settings.py`:

```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
SECRET_KEY = os.environ.get('SECRET_KEY')  # Use environment variables

# For static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

```

2. Collect static files:

```bash
python manage.py collectstatic

```

3. Configure database settings for production.
4. Create a requirements file:

```bash
pip freeze > requirements.txt

```

### Deployment Options

1. **Heroku**

- Create a `Procfile`:

```sh
web: gunicorn projectname.wsgi

```

- Configure database (usually PostgreSQL)
- Push to Heroku

2. **PythonAnywhere**

   - Upload code
   - Set up a virtual environment
   - Configure WSGI file

3. **Docker**

   - Create a `Dockerfile` and `docker-compose.yml`
   - Build and deploy containers

4. **Traditional Hosting**

   - Set up WSGI server (Gunicorn, uWSGI)
   - Configure web server (Nginx, Apache)
   - Set up database

## Best Practices

### Code Organization

- Keep apps small and focused
- Use abstract base classes for common model fields
- Keep views simple; use Django's class-based views when appropriate
- Use model managers for custom query logic

### Security

- Keep `SECRET_KEY` secure and out of version control
- Use environment variables for sensitive information
- Keep `DEBUG = False` in production
- Keep dependencies updated
- Use HTTPS
- Handle user input with care (validate forms)

### Performance

- Use database indexes for frequently queried fields
- Use `select_related()` and `prefetch_related()` to reduce database queries
- Cache expensive operations
- Use pagination for large querysets
- Optimize static and media files (compression, CDN)

### Maintainability

- Write tests
- Document your code
- Follow PEP 8 style guide
- Use version control
- Keep dependencies updated

## Useful Resources

### Official Documentation

- [Django Documentation](https://docs.djangoproject.com/)
- [Django Tutorial](https://docs.djangoproject.com/en/stable/intro/tutorial01/)
- [Django Reference](https://docs.djangoproject.com/en/stable/ref/)
- [Django Admin](https://docs.djangoproject.com/en/stable/ref/contrib/admin/)

### Books

- "Django for Beginners" by William S. Vincent
- "Two Scoops of Django" by Daniel Roy Greenfeld and Audrey Roy Greenfeld
- "Django for Professionals" by William S. Vincent

### Online Courses

- Django course on Coursera, Udemy, or edX
- Django for Everybody by Dr. Chuck Severance
- Django Girls Tutorial

### Communities

- [Django Forum](https://forum.djangoproject.com/)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/django)
- [Reddit Django Community](https://www.reddit.com/r/django/)
- Django Discord Channels

### Tools and Packages

- Django Rest Framework (for APIs)
- Celery (for background tasks)
- Django Debug Toolbar (for development)
- Django Crispy Forms (for better forms)
- Django AllAuth (for authentication)

### Practice Projects

1. **Blog**: Create a blog with posts, comments, and categories
2. **E-commerce Site**: Build a store with products, categories, and a cart
3. **Social Network**: Build profiles, posts, and following relationships
4. **API**: Create a REST API for an existing project
5. **Portfolio Website**: Create your personal portfolio site with Django

---

Remember, learning Django takes time. Start with small projects and gradually work your way up to more complex applications. The Django community is very supportive, so don't hesitate to ask for help when you get stuck!
