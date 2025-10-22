#!/usr/bin/env python
"""
Реалдуу кыргыз маалыматтары менен база толтуруу
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
from core.models import UserProfile, Teacher, Student, Course, Group, Subject, TimeSlot, Schedule

def create_real_data():
    print("🚀 Реалдуу маалыматтарды түзүү башталды...")
    
    # Алдын ала бардыгын тазалайбыз
    print("🧹 Мурунку маалыматтарды тазалоо...")
    User.objects.filter(username__startswith='real_').delete()
    
    # Реалдуу кыргыз аттары
    kyrgyz_names_male = [
        'Азамат', 'Бекжан', 'Дастан', 'Эрмек', 'Жаныбек', 'Канат', 'Марат', 
        'Нурлан', 'Тилек', 'Улан', 'Болот', 'Мирлан', 'Нурбек', 'Кубат',
        'Асан', 'Омур', 'Темир', 'Эльмир', 'Жамшид', 'Салим'
    ]
    
    kyrgyz_names_female = [
        'Айгүл', 'Бермет', 'Гүлмира', 'Динара', 'Жамал', 'Күлайым', 'Медина',
        'Нургүл', 'Салтанат', 'Айжан', 'Гүлнара', 'Жамила', 'Назира', 
        'Салима', 'Тынара', 'Эльмира', 'Асель', 'Бегайым', 'Гүлзат', 'Нурай'
    ]
    
    kyrgyz_surnames = [
        'Абдиев', 'Бейшенов', 'Исаков', 'Кадыров', 'Мамбетов', 'Токтогулов',
        'Эрматов', 'Жумабаев', 'Турсунов', 'Омуров', 'Садыков', 'Исмаилов',
        'Касымов', 'Мусаев', 'Кенжебаев', 'Турдубеков'
    ]
    
    # Курстар
    print("\n📚 Курстарды түзүү...")
    Course.objects.all().delete()
    
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
        course, _ = Course.objects.get_or_create(
            name=name,
            year=year,
            defaults={'faculty': faculty}
        )
        courses.append(course)
    
    print(f"✅ {len(courses)} курс түзүлдү")
    
    # Группалар
    print("\n👥 Группаларды түзүү...")
    Group.objects.all().delete()
    
    group_data = [
        ('КИ-1-21', courses[0], 25),  # 1-курс Компьютерные науки
        ('КИ-2-21', courses[0], 23),
        ('КИ-1-20', courses[1], 28),  # 2-курс Компьютерные науки
        ('КИ-2-20', courses[1], 26),
        ('МА-1-21', courses[2], 30),  # 1-курс Математика
        ('МА-1-20', courses[3], 27),  # 2-курс Математика
        ('ЭК-1-21', courses[4], 32),  # 1-курс Экономика
        ('КФ-1-21', courses[5], 28),  # 1-курс Кыргыз филологиясы
    ]
    
    groups = []
    for name, course, capacity in group_data:
        group, _ = Group.objects.get_or_create(
            name=name,
            course=course,
            defaults={'capacity': capacity}
        )
        groups.append(group)
    
    print(f"✅ {len(groups)} группа түзүлдү")
    
    # Мугалимдер
    print("\n👨‍🏫 Мугалимдерди түзүү...")
    Teacher.objects.all().delete()
    
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
        # User түзөбүз
        username = f"teacher_{first_name.lower()}_{last_name.lower()}"
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
                'email': f"{username}@university.kg",
                'password': 'pbkdf2_sha256$260000$encrypted_password'
            }
        )
        user.set_password('password123')
        user.save()
        
        # UserProfile түзөбүз
        profile, _ = UserProfile.objects.get_or_create(
            user=user,
            defaults={'role': 'TEACHER'}
        )
        
        # Teacher түзөбүз
        teacher, created = Teacher.objects.get_or_create(
            user=user,
            defaults={
                'name': f"{first_name} {last_name}",
                'degree': degree,
                'department': department
            }
        )
        teachers.append(teacher)
        
        if created:
            print(f"  ✅ {teacher.name} ({teacher.get_degree_display()})")
    
    print(f"✅ {len(teachers)} мугалим түзүлдү")
    
    # Студенттер
    print("\n👨‍🎓 Студенттерди түзүү...")
    Student.objects.filter(user__username__startswith='real_').delete()
    
    students = []
    student_count = 0
    
    for group in groups:
        # Ар бир группага 15-20 студент
        group_size = random.randint(15, 20)
        
        for i in range(group_size):
            # Аттарды тандайбыз
            if random.choice([True, False]):  # 50/50 эркек/аял
                first_name = random.choice(kyrgyz_names_male)
            else:
                first_name = random.choice(kyrgyz_names_female)
            
            last_name = random.choice(kyrgyz_surnames)
            
            # Уникалдуу username
            username = f"real_student_{student_count + 1}"
            
            # User түзөбүз
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': f"{username}@student.kg",
                }
            )
            user.set_password('password123')
            user.save()
            
            # UserProfile түзөбүз
            profile, _ = UserProfile.objects.get_or_create(
                user=user,
                defaults={'role': 'STUDENT'}
            )
            
            # Student түзөбүз
            student, created = Student.objects.get_or_create(
                user=user,
                defaults={
                    'name': f"{first_name} {last_name}",
                    'group': group,
                    'student_id': f"ST{2021 + group.course.year}{student_count + 1:04d}"
                }
            )
            
            if created:
                students.append(student)
                student_count += 1
                if student_count <= 5:  # Биринчи 5'ин көрсөтөбүз
                    print(f"    {student.name} -> {group.name}")
        
        print(f"  ✅ {group.name}: {group_size} студент")
    
    print(f"✅ Жалпы {len(students)} студент түзүлдү")
    
    # Ата-энелер
    print("\n👨‍👩‍👧‍👦 Ата-энелерди түзүү...")
    
    parents_created = 0
    for student in students[:50]:  # Биринчи 50 студентке ата-эне
        # Ата
        father_first = random.choice(kyrgyz_names_male)
        father_last = student.name.split()[-1]  # Студенттин фамилиясы
        
        father_username = f"real_father_{parents_created + 1}"
        father_user, created = User.objects.get_or_create(
            username=father_username,
            defaults={
                'first_name': father_first,
                'last_name': father_last,
                'email': f"{father_username}@parent.kg",
            }
        )
        father_user.set_password('password123')
        father_user.save()
        
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
        mother_last = father_last
        
        mother_username = f"real_mother_{parents_created + 1}"
        mother_user, created = User.objects.get_or_create(
            username=mother_username,
            defaults={
                'first_name': mother_first,
                'last_name': mother_last,
                'email': f"{mother_username}@parent.kg",
            }
        )
        mother_user.set_password('password123')
        mother_user.save()
        
        mother_profile, _ = UserProfile.objects.get_or_create(
            user=mother_user,
            defaults={
                'role': 'PARENT',
                'phone': f"+996{random.randint(500000000, 799999999)}",
                'address': f"Бишкек ш., {random.randint(1, 50)}-көчө"
            }
        )
        
        # Ата-эне менен студентти байланыштырабыз
        student.parents.add(father_profile, mother_profile)
        
        parents_created += 1
        
        if parents_created <= 5:  # Биринчи 5'ин көрсөтөбүз
            print(f"  ✅ {father_first} {father_last} жана {mother_first} {mother_last} -> {student.name}")
    
    print(f"✅ {parents_created * 2} ата-эне түзүлдү")
    
    # Сабактар
    print("\n📖 Сабактарды түзүү...")
    Subject.objects.all().delete()
    
    subjects_data = [
        # Компьютерные науки 1-курс (course 0)
        ('Программалоонун негиздери', teachers[0], courses[0]),
        ('Дискреттүү математика', teachers[1], courses[0]),
        ('Компьютердик системалар', teachers[2], courses[0]),
        ('Англис тили', teachers[7], courses[0]),
        ('Кыргыз тили', teachers[3], courses[0]),
        
        # Компьютерные науки 2-курс (course 1)
        ('Маалымат структуралары', teachers[0], courses[1]),
        ('Алгоритмдер жана анализ', teachers[2], courses[1]),
        ('База данных', teachers[6], courses[1]),
        ('Веб программалоо', teachers[8], courses[1]),
        
        # Математика 1-курс (course 2)
        ('Математикалык анализ', teachers[1], courses[2]),
        ('Линейралуу алгебра', teachers[5], courses[2]),
        ('Аналитикалык геометрия', teachers[10], courses[2]),
        
        # Математика 2-курс (course 3)
        ('Дифференциалдык теңдемелер', teachers[1], courses[3]),
        ('Комплекс анализ', teachers[5], courses[3]),
        
        # Экономика (course 4)
        ('Микроэкономика', teachers[4], courses[4]),
        ('Макроэкономика', teachers[9], courses[4]),
        ('Эконометрика', teachers[4], courses[4]),
        ('Каржы математикасы', teachers[9], courses[4]),
        
        # Кыргыз филологиясы (course 5)
        ('Кыргыз адабияты', teachers[3], courses[5]),
        ('Кыргыз тилинин грамматикасы', teachers[11], courses[5]),
        ('Фольклор', teachers[3], courses[5]),
    ]
    
    subjects = []
    for name, teacher, course in subjects_data:
        subject, created = Subject.objects.get_or_create(
            subject_name=name,
            defaults={
                'teacher': teacher,
                'course': course
            }
        )
        subjects.append(subject)
        
        if created:
            print(f"  ✅ {name} -> {teacher.name}")
    
    print(f"✅ {len(subjects)} сабак түзүлдү")
    
    # Убакыт слоттору
    print("\n⏰ Убакыт слотторун түзүү...")
    TimeSlot.objects.all().delete()
    
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
        slot, created = TimeSlot.objects.get_or_create(
            name=name,
            defaults={
                'start_time': start,
                'end_time': end,
                'order': order
            }
        )
        time_slots.append(slot)
    
    print(f"✅ {len(time_slots)} убакыт слоту түзүлдү")
    
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
    print("🎉 Реалдуу маалыматтар ийгиликтүү түзүлдү!")

if __name__ == '__main__':
    create_real_data()