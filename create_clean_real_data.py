#!/usr/bin/env python
"""
База толугу менен тазалап, жаңы реалдуу маалыматтар менен толтуруу
"""

import os
import django
import sys
import random
from datetime import datetime, timedelta

# Django орнотуу
sys.path.append('/Users/k_beknazarovicloud.com/Downloads/su_attendance-main 2')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance_system.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import UserProfile, Teacher, Student, Course, Group, Subject, TimeSlot, Schedule, Attendance

def clean_and_create_real_data():
    print("🚀 База тазалап, жаңы реалдуу маалыматтар түзүү...")
    
    print("🧹 Бардык маалыматтарды тазалоо...")
    # Бардыгын тазалайбыз (ilias admin'ден башка)
    Attendance.objects.all().delete()
    Schedule.objects.all().delete()
    Subject.objects.all().delete()
    TimeSlot.objects.all().delete()
    Student.objects.all().delete()
    Teacher.objects.all().delete()
    Group.objects.all().delete()
    Course.objects.all().delete()
    
    # Admin'ден башка бардык user'лерди өчүрөбүз
    UserProfile.objects.exclude(user__username__in=['ilias', 'admin']).delete()
    User.objects.exclude(username__in=['ilias', 'admin']).delete()
    
    # Реалдуу кыргыз аттары
    kyrgyz_names_male = [
        'Азамат', 'Бекжан', 'Дастан', 'Эрмек', 'Жаныбек', 'Канат', 'Марат', 
        'Нурлан', 'Тилек', 'Улан', 'Болот', 'Мирлан', 'Нурбек', 'Кубат',
        'Асан', 'Омур', 'Темир', 'Эльмир', 'Жамшид', 'Салим', 'Талантбек',
        'Алтынбек', 'Бакыт', 'Нуржан', 'Айбек', 'Эркин', 'Бектур', 'Азиз'
    ]
    
    kyrgyz_names_female = [
        'Айгүл', 'Бермет', 'Гүлмира', 'Динара', 'Жамал', 'Күлайым', 'Медина',
        'Нургүл', 'Салтанат', 'Айжан', 'Гүлнара', 'Жамила', 'Назира', 
        'Салима', 'Тынара', 'Эльмира', 'Асель', 'Бегайым', 'Гүлзат', 'Нурай',
        'Алтынай', 'Бүбүсара', 'Гүлстан', 'Нурзат', 'Айсалкын', 'Төлгөнай'
    ]
    
    kyrgyz_surnames = [
        'Абдиев', 'Бейшенов', 'Исаков', 'Кадыров', 'Мамбетов', 'Токтогулов',
        'Эрматов', 'Жумабаев', 'Турсунов', 'Омуров', 'Садыков', 'Исмаилов',
        'Касымов', 'Мусаев', 'Кенжебаев', 'Турдубеков', 'Алымов', 'Бакиров'
    ]
    
    # 1. Курстар
    print("\n📚 Курстарды түзүү...")
    course_data = [
        ('Компьютерные науки', 1, 'Информатика жана Технологиялар факультети'),
        ('Компьютерные науки', 2, 'Информатика жана Технологиялар факультети'),
        ('Математика', 1, 'Математика жана Физика факультети'),
        ('Математика', 2, 'Математика жана Физика факультети'),
        ('Экономика', 1, 'Экономика жана Менеджмент факультети'),
        ('Кыргыз филологиясы', 1, 'Гуманитардык факультет'),
    ]
    
    courses = []
    for name, year, faculty in course_data:
        course = Course.objects.create(name=name, year=year, faculty=faculty)
        courses.append(course)
        print(f"  ✅ {name} {year}-курс")
    
    # 2. Группалар
    print("\n👥 Группаларды түзүү...")
    group_data = [
        ('КИ-1-21', courses[0], 25),
        ('КИ-2-21', courses[0], 24),
        ('КИ-1-20', courses[1], 22),
        ('КИ-2-20', courses[1], 23),
        ('МА-1-21', courses[2], 20),
        ('МА-1-20', courses[3], 21),
        ('ЭК-1-21', courses[4], 25),
        ('КФ-1-21', courses[5], 18),
    ]
    
    groups = []
    for name, course, capacity in group_data:
        group = Group.objects.create(name=name, course=course, capacity=capacity)
        groups.append(group)
        print(f"  ✅ {name} ({course.name} {course.year}-курс)")
    
    # 3. Мугалимдер
    print("\n👨‍🏫 Мугалимдерди түзүү...")
    teacher_data = [
        ('Токтосун', 'Абдыкеримов', 'PROFESSOR', 'Программалоо кафедрасы'),
        ('Гүлнара', 'Исакова', 'DOCENT', 'Математика кафедрасы'),
        ('Мирлан', 'Токтогулов', 'DOCENT', 'Информатика кафедрасы'),
        ('Салима', 'Жумабаева', 'LECTURER', 'Тил билими кафедрасы'),
        ('Канат', 'Мамбетов', 'LECTURER', 'Экономика кафедрасы'),
        ('Айжан', 'Садыкова', 'LECTURER', 'Математика кафедрасы'),
        ('Нурбек', 'Эрматов', 'ASSISTANT', 'Программалоо кафедрасы'),
        ('Бермет', 'Касымова', 'ASSISTANT', 'Тил билими кафедрасы'),
        ('Асан', 'Турсунов', 'TEACHER', 'Информатика кафедрасы'),
        ('Динара', 'Омурова', 'TEACHER', 'Экономика кафедрасы'),
        ('Жамшид', 'Кенжебаев', 'TEACHER', 'Математика кафедрасы'),
        ('Медина', 'Бейшенова', 'TEACHER', 'Тил билими кафедрасы'),
    ]
    
    teachers = []
    for first_name, last_name, degree, department in teacher_data:
        # User
        username = f"teacher_{first_name.lower()}_{last_name.lower()}"
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=f"{username}@university.kg",
            password='password123'
        )
        
        # UserProfile
        profile, _ = UserProfile.objects.get_or_create(
            user=user,
            defaults={'role': 'TEACHER'}
        )
        
        # Teacher
        teacher = Teacher.objects.create(
            user=user,
            name=f"{first_name} {last_name}",
            degree=degree,
            department=department
        )
        teachers.append(teacher)
        print(f"  ✅ {teacher.name} ({teacher.get_degree_display()})")
    
    # 4. Студенттер
    print("\n👨‍🎓 Студенттерди түзүү...")
    students = []
    student_counter = 1
    
    for group in groups:
        # Ар бир группага 15-20 студент
        group_size = random.randint(15, min(20, group.capacity))
        
        print(f"  🎓 {group.name} үчүн {group_size} студент:")
        
        for i in range(group_size):
            # Аттарды тандайбыз
            if random.choice([True, False]):
                first_name = random.choice(kyrgyz_names_male)
            else:
                first_name = random.choice(kyrgyz_names_female)
            
            last_name = random.choice(kyrgyz_surnames)
            
            # User
            username = f"student_{student_counter}"
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=f"{username}@student.kg",
                password='password123'
            )
            
            # UserProfile
            profile, _ = UserProfile.objects.get_or_create(
                user=user,
                defaults={'role': 'STUDENT'}
            )
            
            # Student
            student, _ = Student.objects.get_or_create(
                user=user,
                defaults={
                    'name': f"{first_name} {last_name}",
                    'group': group,
                    'course': group.course
                }
            )
            
            students.append(student)
            
            if i < 3:  # Биринчи 3үн көрсөтөбүз
                print(f"    ✅ {student.name}")
            
            student_counter += 1
        
        if group_size > 3:
            print(f"    ... жана дагы {group_size - 3} студент")
    
    print(f"✅ Жалпы {len(students)} студент түзүлдү")
    
    # 5. Ата-энелер (биринчи 30 студентке)
    print("\n👨‍👩‍👧‍👦 Ата-энелерди түзүү...")
    parents_count = 0
    
    for student in students[:30]:
        # Ата
        father_first = random.choice(kyrgyz_names_male)
        father_last = student.name.split()[-1]
        
        father_user = User.objects.create_user(
            username=f"father_{parents_count + 1}",
            first_name=father_first,
            last_name=father_last,
            email=f"father_{parents_count + 1}@parent.kg",
            password='password123'
        )
        
        father_profile, _ = UserProfile.objects.get_or_create(
            user=father_user,
            defaults={
                'role': 'PARENT',
                'phone': f"+996{random.randint(500000000, 799999999)}",
                'address': f"Бишкек ш., {random.randint(1, 50)}-көчө"
            }
        )
        
        # Эне
        mother_first = random.choice(kyrgyz_names_female)
        
        mother_user = User.objects.create_user(
            username=f"mother_{parents_count + 1}",
            first_name=mother_first,
            last_name=father_last,
            email=f"mother_{parents_count + 1}@parent.kg",
            password='password123'
        )
        
        mother_profile, _ = UserProfile.objects.get_or_create(
            user=mother_user,
            defaults={
                'role': 'PARENT',
                'phone': f"+996{random.randint(500000000, 799999999)}",
                'address': f"Бишкек ш., {random.randint(1, 50)}-көчө"
            }
        )
        
        # Студент менен байланыштырабыз
        student.parents.add(father_profile, mother_profile)
        
        if parents_count < 5:
            print(f"  ✅ {father_first} {father_last} ж/а {mother_first} {father_last} -> {student.name}")
        
        parents_count += 1
    
    print(f"✅ {parents_count * 2} ата-эне түзүлдү")
    
    # 6. Сабактар
    print("\n📖 Сабактарды түзүү...")
    subjects_data = [
        # КИ 1-курс
        ('Программалоонун негиздери', teachers[0], courses[0]),
        ('Дискреттүү математика', teachers[1], courses[0]),
        ('Компьютердик системалар', teachers[2], courses[0]),
        ('Англис тили', teachers[7], courses[0]),
        ('Кыргыз тили', teachers[3], courses[0]),
        
        # КИ 2-курс
        ('Маалымат структуралары', teachers[0], courses[1]),
        ('Алгоритмдер жана анализ', teachers[2], courses[1]),
        ('База данных', teachers[6], courses[1]),
        ('Веб программалоо', teachers[8], courses[1]),
        
        # Математика 1-курс
        ('Математикалык анализ', teachers[1], courses[2]),
        ('Линейралуу алгебра', teachers[5], courses[2]),
        ('Аналитикалык геометрия', teachers[10], courses[2]),
        
        # Математика 2-курс
        ('Дифференциалдык теңдемелер', teachers[1], courses[3]),
        ('Комплекс анализ', teachers[5], courses[3]),
        
        # Экономика
        ('Микроэкономика', teachers[4], courses[4]),
        ('Макроэкономика', teachers[9], courses[4]),
        ('Эконометрика', teachers[4], courses[4]),
        
        # Кыргыз филологиясы
        ('Кыргыз адабияты', teachers[3], courses[5]),
        ('Кыргыз тилинин грамматикасы', teachers[11], courses[5]),
        ('Фольклор', teachers[3], courses[5]),
    ]
    
    subjects = []
    for name, teacher, course in subjects_data:
        subject = Subject.objects.create(
            subject_name=name,
            teacher=teacher,
            course=course
        )
        subjects.append(subject)
        print(f"  ✅ {name} -> {teacher.name}")
    
    # 7. Убакыт слоттору
    print("\n⏰ Убакыт слотторун түзүү...")
    time_slots_data = [
        ('1-пара', '08:30', '10:00', 1),
        ('2-пара', '10:15', '11:45', 2),
        ('3-пара', '12:00', '13:30', 3),
        ('4-пара', '14:15', '15:45', 4),
        ('5-пара', '16:00', '17:30', 5),
        ('6-пара', '17:45', '19:15', 6),
    ]
    
    time_slots = []
    for name, start, end, order in time_slots_data:
        slot = TimeSlot.objects.create(
            name=name,
            start_time=start,
            end_time=end,
            order=order
        )
        time_slots.append(slot)
        print(f"  ✅ {name} ({start}-{end})")
    
    print("\n============================================================")
    print("📊 ЖЫЙЫНТЫК:")
    print("============================================================")
    print(f"👥 Колдонуучулар: {User.objects.count()}")
    print(f"👨‍🏫 Мугалимдер: {Teacher.objects.count()}")
    print(f"👨‍🎓 Студенттер: {Student.objects.count()}")
    print(f"👨‍👩‍👧‍👦 Ата-энелер: {UserProfile.objects.filter(role='PARENT').count()}")
    print(f"📚 Курстар: {Course.objects.count()}")
    print(f"👥 Группалар: {Group.objects.count()}")
    print(f"📖 Сабактар: {Subject.objects.count()}")
    print(f"⏰ Убакыт слоттору: {TimeSlot.objects.count()}")
    print("============================================================")
    print()
    print("✨ Бардык колдонуучулардын сыр сөзү: password123")
    print()
    print("🎉 Жаңы реалдуу маалыматтар ийгиликтүү түзүлдү!")

if __name__ == '__main__':
    clean_and_create_real_data()