#!/usr/bin/env python
"""
Тест колдонуучуларды түзүү скрипти
100 user: 10 teacher, 50 student, 40 parent
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

def create_test_data():
    print("🚀 Тест маалыматтарын түзүү башталды...")
    
    # Курстар жана группалар
    print("\n📚 Курстарды түзүү...")
    course1, _ = Course.objects.get_or_create(
        name='Информатика',
        year=1,
        defaults={'faculty': 'Информатика жана Технологиялар'}
    )
    course2, _ = Course.objects.get_or_create(
        name='Математика',
        year=2,
        defaults={'faculty': 'Математика жана Физика'}
    )
    course3, _ = Course.objects.get_or_create(
        name='Экономика',
        year=1,
        defaults={'faculty': 'Экономика жана Бизнес'}
    )
    
    print("✅ 3 курс түзүлдү")
    
    # Группалар
    print("\n👥 Группаларды түзүү...")
    groups = []
    group_names = ['CS-11', 'CS-12', 'CS-13', 'MATH-21', 'MATH-22', 'ECO-11', 'ECO-12']
    courses = [course1, course1, course1, course2, course2, course3, course3]
    
    for name, course in zip(group_names, courses):
        group, _ = Group.objects.get_or_create(
            name=name,
            course=course
        )
        groups.append(group)
    
    print(f"✅ {len(groups)} группа түзүлдү")
    
    # 10 МУГАЛИМ
    print("\n👨‍🏫 10 мугалимди түзүү...")
    teacher_names = [
        'Алмаз Касымов', 'Айжан Токтогулова', 'Нурбек Эрматов',
        'Гүлнара Жумабаева', 'Эрлан Турдубеков', 'Асель Кенжебаева',
        'Марат Садыков', 'Жамила Исмаилова', 'Тилек Бейшенов', 'Динара Мусаева'
    ]
    
    degrees = ['PROFESSOR', 'DOCENT', 'LECTURER', 'ASSISTANT', 'TEACHER']
    
    for i, name in enumerate(teacher_names, 1):
        username = f'teacher{i}'
        
        # User түзүү
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'first_name': name.split()[0],
                'last_name': name.split()[1],
                'email': f'{username}@university.edu.kg',
                'is_active': True
            }
        )
        if created:
            user.set_password('password123')
            user.save()
        
        # UserProfile түзүү
        profile, _ = UserProfile.objects.get_or_create(
            user=user,
            defaults={'role': 'TEACHER'}
        )
        
        # Teacher түзүү
        teacher, _ = Teacher.objects.get_or_create(
            user=user,
            defaults={
                'name': name,
                'degree': degrees[i % len(degrees)],
                'department': 'Кафедра ' + str((i % 3) + 1)
            }
        )
        
        if created:
            print(f"  ✅ {name} ({username}) - {teacher.get_degree_display()}")
    
    print(f"✅ 10 мугалим түзүлдү")
    
    # 50 СТУДЕНТ
    print("\n👨‍🎓 50 студентти түзүү...")
    first_names = [
        'Азамат', 'Бекжан', 'Дастан', 'Эрмек', 'Жаныбек',
        'Айгүл', 'Бермет', 'Гүлмира', 'Динара', 'Эльмира',
        'Канат', 'Марат', 'Нурлан', 'Тилек', 'Улан',
        'Жамал', 'Күлайым', 'Медина', 'Нургүл', 'Салтанат'
    ]
    
    last_names = [
        'Абдиев', 'Бейшенов', 'Исаков', 'Кадыров', 'Мамбетов',
        'Токтогулова', 'Эрматова', 'Жумабаева', 'Турсунова', 'Омурова'
    ]
    
    student_count = 0
    for i in range(50):
        username = f'student{i+1}'
        first = first_names[i % len(first_names)]
        last = last_names[i % len(last_names)]
        full_name = f'{first} {last}'
        
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
        
        # Группаны тандоо
        group = groups[i % len(groups)]
        
        # Student түзүү
        student, _ = Student.objects.get_or_create(
            user=user,
            defaults={
                'name': full_name,
                'course': group.course,
                'group': group
            }
        )
        
        if created:
            student_count += 1
            if student_count % 10 == 0:
                print(f"  ✅ {student_count} студент түзүлдү...")
    
    print(f"✅ 50 студент түзүлдү")
    
    # 40 АТА-ЭНЕ
    print("\n👨‍👩‍👧‍👦 40 ата-энени түзүү...")
    parent_first_names = [
        'Асан', 'Болот', 'Дмитрий', 'Кубат', 'Мирлан',
        'Гүлнара', 'Жамила', 'Назира', 'Салима', 'Тынара'
    ]
    
    parent_count = 0
    students = list(Student.objects.all()[:40])  # Биринчи 40 студент
    
    for i in range(40):
        username = f'parent{i+1}'
        first = parent_first_names[i % len(parent_first_names)]
        last = last_names[i % len(last_names)]
        
        # User түзүү
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'first_name': first,
                'last_name': last,
                'email': f'{username}@parent.university.edu.kg',
                'is_active': True
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            parent_count += 1
        
        # UserProfile түзүү - бул жерде роль туура коюлуу керек
        profile, prof_created = UserProfile.objects.get_or_create(
            user=user,
            defaults={'role': 'PARENT'}
        )
        
        # Эгер мурда башка роль менен түзүлсө, роль өзгөртүү
        if not prof_created and profile.role != 'PARENT':
            profile.role = 'PARENT'
            profile.save()
        
        # Студентке байланыштыруу
        if i < len(students):
            profile.students.add(students[i])
            print(f"  ✅ {user.get_full_name()} -> {students[i].name}")
        
        if parent_count % 10 == 0 and parent_count > 0:
            print(f"  ✅ {parent_count} ата-эне түзүлдү...")
    
    print(f"✅ {parent_count} ата-эне түзүлдү")
    
    # Жыйынтык
    print("\n" + "="*60)
    print("📊 ЖЫЙЫНТЫК:")
    print("="*60)
    print(f"👥 Бардык колдонуучулар: {User.objects.count()}")
    print(f"👨‍🏫 Мугалимдер: {Teacher.objects.count()}")
    print(f"👨‍🎓 Студенттер: {Student.objects.count()}")
    print(f"👨‍👩‍👧‍👦 Ата-энелер: {UserProfile.objects.filter(role='PARENT').count()}")
    print(f"📚 Курстар: {Course.objects.count()}")
    print(f"👥 Группалар: {Group.objects.count()}")
    print("="*60)
    print("\n✨ Бардык колдонуучулардын сыр сөзү: password123")
    print("\n🎉 Тест маалыматтары ийгиликтүү түзүлдү!")

if __name__ == '__main__':
    try:
        create_test_data()
    except Exception as e:
        print(f"\n❌ Ката: {e}")
        import traceback
        traceback.print_exc()
