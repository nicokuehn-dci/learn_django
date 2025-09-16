from django.contrib import admin
from .models import Project, Stage, Task

# Register your models here.

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
