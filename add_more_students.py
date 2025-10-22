#!/usr/bin/env python
"""
Группаларга туура бөлүштүрүлгөн кошумча студенттерди түзүү
"""

import os
import django
import sys

# Django орнотуу
sys.path.append('/Users/k_beknazarovicloud.com/Downloads/su_attendance-main 2')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance_system.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import UserProfile, Student, Course, Group

print("🚀 Кошумча студенттерди түзүү...")

# Группаларды алуу
groups = list(Group.objects.filter(name__in=['CS-11', 'CS-12', 'CS-13', 'MATH-21', 'MATH-22', 'ECO-11', 'ECO-12']))

first_names = [
    'Азамат', 'Бекжан', 'Дастан', 'Эрмек', 'Жаныбек',
    'Айгүл', 'Бермет', 'Гүлмира', 'Динара', 'Эльмира',
    'Канат', 'Марат', 'Нурлан', 'Тилек', 'Улан',
    'Жамал', 'Күлайым', 'Медина', 'Нургүл', 'Салтанат',
    'Темир', 'Бакыт', 'Нурбол', 'Элдияр', 'Алтынбек'
]

last_names = [
    'Абдиев', 'Бейшенов', 'Исаков', 'Кадыров', 'Мамбетов',
    'Токтогулова', 'Эрматова', 'Жумабаева', 'Турсунова', 'Омурова',
    'Садыков', 'Асанов', 'Усенов', 'Мурзалиев', 'Ташиев'
]

# Учурдагы студенттердин санын алуу
current_count = Student.objects.count()
start_number = 51  # student51ден баштайбыз

students_per_group = 50 // len(groups)  # Ар бир группага 7 студент
extra = 50 % len(groups)  # Калган студенттер

created_count = 0

for idx, group in enumerate(groups):
    count_for_group = students_per_group + (1 if idx < extra else 0)
    
    print(f"\n📚 {group.name} группасына {count_for_group} студент кошуу...")
    
    for i in range(count_for_group):
        student_num = start_number + created_count
        username = f'student{student_num}'
        
        first = first_names[created_count % len(first_names)]
        last = last_names[created_count % len(last_names)]
        full_name = f'{first} {last} {created_count+1}'
        
        # User түзүү
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'first_name': first,
                'last_name': last,
                'email': f'{username}@student.university.edu.kg',
                'is_active': True
            }
        )
        if created:
            user.set_password('password123')
            user.save()
        
        # UserProfile түзүү
        profile, _ = UserProfile.objects.get_or_create(
            user=user,
            defaults={'role': 'STUDENT'}
        )
        
        # Student түзүү
        student, stud_created = Student.objects.get_or_create(
            user=user,
            defaults={
                'name': full_name,
                'course': group.course,
                'group': group
            }
        )
        
        if stud_created:
            created_count += 1
            print(f"  ✅ {full_name} ({username}) -> {group.name}")

print(f"\n✅ Жалпы {created_count} студент кошулду")
print(f"📊 Азыр бардыгы {Student.objects.count()} студент")

# Группалар боюнча статистика
print("\n📈 ГРУППАЛАР БОЮНЧА СТАТИСТИКА:")
print("-" * 60)
for group in groups:
    count = Student.objects.filter(group=group).count()
    print(f"  {group.name}: {count} студент")
