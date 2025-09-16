# Django Practice Project - Learn Django

A comprehensive Django project demonstrating project management and student management systems with PostgreSQL database integration.

## 📋 Project Overview

This Django project was created as a learning exercise to understand Django framework fundamentals, database modeling, admin interface, and PostgreSQL integration. The project consists of two main applications:

1. **Main App**: Project management system with Projects, Stages, and Tasks
2. **Students App**: Student management system

## 🚀 Features

### Main Application (Project Management)
- **Projects**: Create and manage projects with descriptions and timestamps
- **Stages**: Define workflow stages with ordering
- **Tasks**: Assign tasks to projects, users, and stages with detailed tracking
- **Relationships**: Full foreign key relationships between models
- **Admin Interface**: Custom admin configuration for easy data management

### Students Application
- **Student Management**: Store student information (first name, last name, nickname)
- **Admin Integration**: Full admin interface support

## 🛠 Technical Stack

- **Framework**: Django 5.2.6
- **Database**: PostgreSQL
- **Python**: Python 3.13
- **Environment**: Virtual environment (practice_venv)
- **Dependencies**: psycopg2-binary for PostgreSQL connection

## 📁 Project Structure

```
django_practice/
├── practice_project/          # Main project settings
│   ├── settings.py           # Django configuration with PostgreSQL
│   ├── urls.py              # URL routing
│   └── wsgi.py              # WSGI configuration
├── main/                     # Project management app
│   ├── models.py            # Project, Stage, Task models
│   ├── admin.py             # Admin interface configuration
│   ├── views.py             # View functions
│   └── migrations/          # Database migrations
├── students/                 # Student management app
│   ├── models.py            # Student model
│   ├── admin.py             # Admin configuration
│   └── migrations/          # Database migrations
├── practice_venv/           # Virtual environment
├── script.py               # Django ORM demonstration script
├── manage.py               # Django management commands
└── requirements.txt        # Project dependencies
```

## 🗃 Database Models

### Main App Models

#### Project Model
```python
class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
```

#### Stage Model
```python
class Stage(models.Model):
    name = models.CharField(max_length=100)
    order_no = models.IntegerField()
```

#### Task Model
```python
class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    assignee = models.ForeignKey(User, on_delete=models.CASCADE)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### Students App Models

#### Student Model
```python
class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=50, blank=True)
```

## 🚀 Setup Instructions

### Prerequisites
- Python 3.13+
- PostgreSQL
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/nicokuehn-dci/learn_django.git
   cd learn_django
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv practice_venv
   source practice_venv/bin/activate  # On Linux/Mac
   # practice_venv\Scripts\activate   # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database Setup**
   ```bash
   # Create PostgreSQL database
   sudo -u postgres createdb django_practice
   
   # Run migrations
   python manage.py migrate
   
   # Create superuser
   python manage.py createsuperuser
   ```

5. **Run the development server**
   ```bash
   python manage.py runserver 8001
   ```

6. **Access the application**
   - Main site: http://127.0.0.1:8001/
   - Admin panel: http://127.0.0.1:8001/admin/

## 💻 Usage Examples

### Django Shell Operations

```python
# Import models
from main.models import Project, Stage, Task
from students.models import Student
from django.contrib.auth.models import User

# Create objects
project = Project.objects.create(
    name="Sample Project",
    description="A sample project for testing"
)

stage = Stage.objects.create(
    name="In Progress",
    order_no=2
)

# Query objects
all_projects = Project.objects.all()
recent_tasks = Task.objects.filter(created_at__gte='2025-01-01')
```

### Management Commands

```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Open Django shell
python manage.py shell

# Run development server
python manage.py runserver 8001

# Show migration status
python manage.py showmigrations
```

## 🗂 Database Configuration

The project uses PostgreSQL with the following configuration:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'django_practice',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 📚 Learning Objectives Achieved

- ✅ Django project setup and configuration
- ✅ Virtual environment management
- ✅ PostgreSQL database integration
- ✅ Django model creation with relationships
- ✅ Database migrations
- ✅ Django admin interface customization
- ✅ Django ORM operations
- ✅ Multi-app Django project structure
- ✅ Git version control and GitHub integration
- ✅ Django shell scripting

## 🔧 Development Tools

- **Virtual Environment**: Isolated Python environment
- **Django Admin**: Web-based interface for data management
- **Django Shell**: Interactive Python console with Django context
- **Git**: Version control with GitHub integration
- **PostgreSQL**: Production-ready database system

## 📖 Documentation Files

- `students/README.md`: Students app specific documentation
- `Django_Learning_Guide.md`: Step-by-step learning guide

## 🤝 Contributing

This is a learning project, but contributions and suggestions are welcome:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is for educational purposes. Feel free to use it for learning Django!

## 👤 Author

**Nico Kühn** - [GitHub Profile](https://github.com/nicokuehn-dci)

---

*This project demonstrates fundamental Django concepts including models, admin interface, database relationships, and PostgreSQL integration. Perfect for Django beginners looking to understand real-world application structure.*
