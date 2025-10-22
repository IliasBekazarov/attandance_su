#!/usr/bin/env python
"""
Сабактарды жана мугалим-сабак байланышын түзүү
"""

import os
import django
import sys

# Django орнотуу
sys.path.append('/Users/k_beknazarovicloud.com/Downloads/su_attendance-main 2')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance_system.settings')
django.setup()

from core.models import Teacher, Subject, Course

print("📚 Сабактарды жана мугалим-сабак байланышын түзүү...")

# Мугалимдерди алуу
teachers = list(Teacher.objects.all())
print(f"Табылган мугалимдер: {len(teachers)}")

# Курстарды алуу
courses = list(Course.objects.all())
print(f"Табылган курстар: {len(courses)}")

if not teachers:
    print("❌ Мугалимдер табылган жок!")
    exit()

if not courses:
    print("❌ Курстар табылган жок!")
    exit()

# Сабактардын тизмеси
subjects_data = [
    # Информатика курсу
    {'name': 'Программалоо негиздери', 'course': 'Информатика'},
    {'name': 'Маалымат структуралары', 'course': 'Информатика'},
    {'name': 'Алгоритмдер', 'course': 'Информатика'},
    {'name': 'Веб-программалоо', 'course': 'Информатика'},
    {'name': 'База данных', 'course': 'Информатика'},
    
    # Математика курсу
    {'name': 'Математикалык анализ', 'course': 'Математика'},
    {'name': 'Линейралуу алгебра', 'course': 'Математика'},
    {'name': 'Геометрия', 'course': 'Математика'},
    {'name': 'Статистика', 'course': 'Математика'},
    
    # Экономика курсу
    {'name': 'Микроэкономика', 'course': 'Экономика'},
    {'name': 'Макроэкономика', 'course': 'Экономика'},
    {'name': 'Эсеп-китеп', 'course': 'Экономика'},
    {'name': 'Маркетинг', 'course': 'Экономика'},
    
    # Жалпы сабактар
    {'name': 'Кыргыз тили', 'course': None},
    {'name': 'Орус тили', 'course': None},
    {'name': 'Англис тили', 'course': None},
    {'name': 'Тарых', 'course': None},
    {'name': 'Физика', 'course': None},
]

created_count = 0

for subject_data in subjects_data:
    course = None
    if subject_data['course']:
        try:
            course = Course.objects.get(name=subject_data['course'])
        except Course.DoesNotExist:
            print(f"⚠️  Курс табылган жок: {subject_data['course']}")
            continue
    else:
        # Жалпы сабактар үчүн биринчи курсту алабыз
        course = courses[0]
    
    # Сабакты түзүү же табуу
    subject, created = Subject.objects.get_or_create(
        subject_name=subject_data['name'],
        course=course,
        defaults={
            'teacher': teachers[created_count % len(teachers)]  # Мугалимдерди кезектештирип дайындайбыз
        }
    )
    
    if created:
        created_count += 1
        print(f"  ✅ {subject.subject_name} -> {subject.teacher.name}")

print(f"\n✅ {created_count} сабак түзүлдү")

# Статистика
print("\n📊 САБАК-МУГАЛИМ СТАТИСТИКАСЫ:")
print("-" * 60)

for teacher in teachers:
    subjects = Subject.objects.filter(teacher=teacher)
    print(f"👨‍🏫 {teacher.name}: {subjects.count()} сабак")
    for subject in subjects:
        print(f"   • {subject.subject_name}")

print(f"\n📚 Жалпы сабактар: {Subject.objects.count()}")