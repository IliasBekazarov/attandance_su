#!/usr/bin/env python
"""
Бардык колдонуучулардын толук отчёту
"""

import os
import django
import sys

# Django орнотуу
sys.path.append('/Users/k_beknazarovicloud.com/Downloads/su_attendance-main 2')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance_system.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import UserProfile, Teacher, Student, Course, Group

print("\n" + "="*70)
print("📊 ATTENDANCE SYSTEM - КОЛДОНУУЧУЛАРДЫН ТОЛУК ОТЧЁТУ")
print("="*70)

print("\n🎯 БАРДЫК КОЛДОНУУЧУЛАР:")
print("-" * 70)
print(f"  👥 Жалпы: {User.objects.count()} колдонуучу")
print(f"  ✅ Активдүү: {User.objects.filter(is_active=True).count()}")
print(f"  ❌ Активдүү эмес: {User.objects.filter(is_active=False).count()}")

print("\n👨‍🏫 МУГАЛИМДЕР:")
print("-" * 70)
teachers = Teacher.objects.all()
print(f"  Жалпы: {teachers.count()} мугалим")
for teacher in teachers:
    print(f"    • {teacher.name} ({teacher.user.username}) - {teacher.get_degree_display()}")

print("\n👨‍🎓 СТУДЕНТТЕР:")
print("-" * 70)
students = Student.objects.all()
print(f"  Жалпы: {students.count()} студент")
groups_dict = {}
for student in students:
    group_name = student.group.name
    if group_name not in groups_dict:
        groups_dict[group_name] = []
    groups_dict[group_name].append(student.name)

for group_name in sorted(groups_dict.keys()):
    print(f"\n  📚 {group_name} ({len(groups_dict[group_name])} студент):")
    for student_name in groups_dict[group_name][:5]:
        print(f"    • {student_name}")
    if len(groups_dict[group_name]) > 5:
        print(f"    ... жана дагы {len(groups_dict[group_name]) - 5} студент")

print("\n👨‍👩‍👧‍👦 АТА-ЭНЕЛЕР:")
print("-" * 70)
parents = UserProfile.objects.filter(role='PARENT')
print(f"  Жалпы: {parents.count()} ата-эне")
for parent in parents[:10]:
    children = parent.students.all()
    print(f"    • {parent.user.get_full_name()} ({parent.user.username})")
    print(f"      Балдары: {', '.join([s.name for s in children[:3]])}")
    if children.count() > 3:
        print(f"      ... жана дагы {children.count() - 3} студент")

print("\n📚 КУРСТАР ЖАНА ГРУППАЛАР:")
print("-" * 70)
courses = Course.objects.all()
print(f"  Жалпы курстар: {courses.count()}")
for course in courses:
    groups = Group.objects.filter(course=course)
    students_count = Student.objects.filter(course=course).count()
    print(f"    • {course.name} ({course.year}-курс)")
    print(f"      Группалар: {groups.count()} | Студенттер: {students_count}")

print("\n🔐 КИРҮҮ МААЛЫМАТТАРЫ:")
print("-" * 70)
print("  Бардык колдонуучулардын сыр сөзү: password123")
print("\n  Мисалдар:")
print("    Админ: admin / admin123")
print("    Мугалим: teacher1 / password123")
print("    Студент: student1 / password123")
print("    Ата-эне: parent1 / password123")

print("\n" + "="*70)
print("✅ Отчёт аяктады!")
print("="*70 + "\n")
