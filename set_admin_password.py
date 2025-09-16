#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'practice_project.settings')
django.setup()

from django.contrib.auth.models import User

# Update or create admin user
try:
    user = User.objects.get(username='admin')
    user.set_password('postgres')
    user.save()
    print('✅ Successfully updated admin password')
except User.DoesNotExist:
    user = User.objects.create_superuser('admin', 'admin@example.com', 'postgres')
    print('✅ Successfully created admin user')

print('\n🔐 Admin Login Credentials:')
print('Username: admin')
print('Password: postgres')
print('URL: http://127.0.0.1:8001/admin/')
print('\n🚀 You can now login to the Django admin panel!')
