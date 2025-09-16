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
