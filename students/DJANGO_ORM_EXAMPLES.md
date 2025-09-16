# Django ORM Query Examples - Students App

This document demonstrates various Django ORM queries using the Student model from the students app.

## Student Model

The Student model has the following fields:
```python
class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
```

## Basic Queries

### 1. Exact Match Filtering

Find all students with a specific first name:
```python
Student.objects.filter(first_name='Elizabeth')
```
**SQL Equivalent:** `SELECT * FROM students_student WHERE first_name = 'Elizabeth'`

### 2. String Pattern Matching

#### Case-Sensitive String Endings
Find students whose last name ends with "ll":
```python
Student.objects.filter(last_name__endswith="ll")
```
**SQL Equivalent:** `SELECT * FROM students_student WHERE last_name LIKE '%ll'`

#### Case-Insensitive String Endings
Find students whose last name ends with "ll" (case-insensitive):
```python
Student.objects.filter(last_name__iendswith="ll")
```
**SQL Equivalent:** `SELECT * FROM students_student WHERE last_name ILIKE '%ll'`

#### Case-Insensitive String Beginnings
Find students whose first name starts with "a":
```python
Student.objects.filter(first_name__istartswith="a")
```
**SQL Equivalent:** `SELECT * FROM students_student WHERE first_name ILIKE 'a%'`

## Counting Records

### Count All Students
```python
Student.objects.count()
```
**SQL Equivalent:** `SELECT COUNT(*) FROM students_student`

### Count with Filtering
Count students whose first name starts with "a":
```python
Student.objects.filter(first_name__istartswith="a").count()
```
**SQL Equivalent:** `SELECT COUNT(*) FROM students_student WHERE first_name ILIKE 'a%'`

## Delete Operations

### Delete with Filtering
Delete all students whose first name starts with "a":
```python
Student.objects.filter(first_name__istartswith="a").delete()
```
**SQL Equivalent:** `DELETE FROM students_student WHERE first_name ILIKE 'a%'`

**Returns:** A tuple `(number_deleted, details_dict)` showing how many objects were deleted.

## Django Field Lookups Reference

### String Lookups
- `__exact` - Exact match (default behavior)
- `__iexact` - Case-insensitive exact match
- `__contains` - Case-sensitive containment test
- `__icontains` - Case-insensitive containment test
- `__startswith` - Case-sensitive starts-with
- `__istartswith` - Case-insensitive starts-with
- `__endswith` - Case-sensitive ends-with
- `__iendswith` - Case-insensitive ends-with

### Numeric Lookups
- `__gt` - Greater than
- `__gte` - Greater than or equal to
- `__lt` - Less than
- `__lte` - Less than or equal to
- `__range` - Range test (between two values)

### List Lookups
- `__in` - In a given list
- `__isnull` - Is null test

## Sample Data Generation

The following script creates 100 random students:

```python
import random
from students.models import Student

first_names = [
    "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
    "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
    "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy", "Daniel", "Lisa",
    "Matthew", "Betty", "Anthony", "Margaret", "Mark", "Sandra", "Donald", "Ashley",
    "Steven", "Kimberly", "Paul", "Emily", "Andrew", "Donna", "Joshua", "Michelle",
    "Kenneth", "Dorothy", "Kevin", "Carol", "Brian", "Amanda", "George", "Melissa",
    "Edward", "Deborah"
]

last_names = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
    "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
    "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker",
    "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
    "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell", "Carter"
]

nicknames = [
    "Ace", "Bear", "Champ", "Duke", "Flash", "Jazz", "Kit", "Maverick", "Ninja", "Oz",
    "Pip", "Rocky", "Scout", "Tex", "Viper", "Wolf", "Ziggy", "Buzz", "Dash", "Echo",
    "Finn", "Gizmo", "Hawk", "Indy", "Jax", "Koda", "Lucky", "Mojo", "Nova", "Otis",
    "Pax", "Quinn", "Rex", "Sky", "Taz", "Uno", "Vega", "Wren", "Yogi", "Zane",
    "Blue", "Coco", "Daisy", "Frost", "Goldie", "Honey", "Ivy", "Juno", "Luna", "Misty"
]

for _ in range(100):
    first = random.choice(first_names)
    last = random.choice(last_names)
    nick = random.choice(nicknames)
    Student.objects.create(first_name=first, last_name=last, nickname=nick)
```

## Testing in Django Shell

To test these queries, open the Django shell:
```bash
python manage.py shell
```

Then import the model and run your queries:
```python
from students.models import Student

# Your queries here
Student.objects.filter(first_name='Elizabeth').count()
```
