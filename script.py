import random
from main.models import Project, Stage, Task
from students.models import Student
from django.contrib.auth.models import User

# === MAIN APP DATA CREATION ===

p = Project.objects.filter(name='AI System').first()
if not p:
    p = Project.objects.create(name='AI System', description='Build some agentic AI')

# stage creation

todo = Stage.objects.filter(name='To Do').first()
if not todo:
    todo = Stage.objects.create(name='To Do', order_no=1)

in_progress = Stage.objects.filter(name='In Progress').first()
if not in_progress:
    in_progress = Stage.objects.create(name='In Progress', order_no=2)


# task
task_1 = Task.objects.filter(title="Setup a django project for developers").first()
if not task_1:
    task_1 = Task.objects.create(title="Setup a django project for developers", project=p, stage=todo)

# Assign a task to a random User for now (e.g. first user in system)
user = User.objects.first()
if user and not task_1.assignee:
    task_1.assignee = user
    task_1.save()

# === STUDENTS APP DATA CREATION ===

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
