#!/usr/bin/env python
"""
Базаны тазалап, жаңы маалыматтарды түзүү
"""

import os
import django
import sys

# Django орнотуу
sys.path.append('/Users/k_beknazarovicloud.com/Downloads/su_attendance-main 2')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance_system.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import UserProfile, Teacher, Student, Course, Group, Subject, Schedule, Attendance

print("⚠️  ЭСКЕРТҮҮ: Бардык тест маалыматтары өчүрүлөт!")
print("Админ жана эски маалыматтар сакталат.")

# Тест колдонуучуларды өчүрүү
print("\n🗑️  Тест колдонуучуларды өчүрүү...")

test_users = User.objects.filter(username__startswith='teacher') | \
             User.objects.filter(username__startswith='student') | \
             User.objects.filter(username__startswith='parent')

count = test_users.count()
test_users.delete()

print(f"✅ {count} тест колдонуучу өчүрүлдү")

# Тест курстарды өчүрүү
print("\n🗑️  Тест курстарды өчүрүү...")
test_courses = Course.objects.filter(name__in=['Информатика', 'Математика', 'Экономика'])
test_courses.delete()
print("✅ Тест курстар өчүрүлдү")

print("\n✅ База тазаланды! Эми жаңы маалыматтарды түзө аласыз.")
print("Жүргүзүңүз: python3 create_test_users.py")
