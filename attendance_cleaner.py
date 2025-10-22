#!/usr/bin/env python
"""
Attendance маалыматтарын селективдүү тазалоо скрипти
Опциялар менен ар кандай тазалоо ыкмалары
"""

import os
import django
import sys
from datetime import datetime, date

# Django орнотуу
sys.path.append('/Users/k_beknazarovicloud.com/Downloads/su_attendance-main 2')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance_system.settings')
django.setup()

from core.models import Attendance

def clean_attendance_data():
    print("🔧 ATTENDANCE ТАЗАЛОО ОПЦИЯЛАРЫ:")
    print("1. Бардык Absent/Late/Excused жазууларын өчүрүү")
    print("2. Белгилүү датадан мурунку бардык жазууларды өчүрүү")
    print("3. Белгилүү статусту гана өчүрүү")
    print("4. Бардык attendance жазууларын өчүрүү")
    print("5. Статистиканы көрүү (өчүрбөстөн)")
    
    choice = input("\nТандооңузду киргизиңиз (1-5): ")
    
    if choice == "1":
        # Present болбогон бардыгын өчүрүү
        non_present = Attendance.objects.exclude(status='Present')
        count = non_present.count()
        
        if count > 0:
            confirm = input(f"⚠️  {count} жазууну өчүрөсүзбү? (yes/no): ")
            if confirm.lower() in ['yes', 'y', 'ооба']:
                non_present.delete()
                print(f"✅ {count} жазуу өчүрүлдү")
            else:
                print("❌ Операция жокко чыгарылды")
        else:
            print("ℹ️  Өчүрүүгө жазуу жок")
    
    elif choice == "2":
        # Датадан мурунку жазууларды өчүрүү
        date_str = input("Дата киргизиңиз (YYYY-MM-DD): ")
        try:
            target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            old_records = Attendance.objects.filter(date__lt=target_date)
            count = old_records.count()
            
            if count > 0:
                confirm = input(f"⚠️  {target_date}дан мурунку {count} жазууну өчүрөсүзбү? (yes/no): ")
                if confirm.lower() in ['yes', 'y', 'ооба']:
                    old_records.delete()
                    print(f"✅ {count} жазуу өчүрүлдү")
                else:
                    print("❌ Операция жокко чыгарылды")
            else:
                print("ℹ️  Өчүрүүгө жазуу жок")
        except ValueError:
            print("❌ Туура эмес дата форматы")
    
    elif choice == "3":
        # Белгилүү статусту өчүрүү
        print("Өчүрүүчү статус:")
        print("1. Absent")
        print("2. Late") 
        print("3. Excused")
        
        status_choice = input("Тандооңуз (1-3): ")
        status_map = {'1': 'Absent', '2': 'Late', '3': 'Excused'}
        
        if status_choice in status_map:
            status = status_map[status_choice]
            records = Attendance.objects.filter(status=status)
            count = records.count()
            
            if count > 0:
                confirm = input(f"⚠️  {count} '{status}' жазууну өчүрөсүзбү? (yes/no): ")
                if confirm.lower() in ['yes', 'y', 'ооба']:
                    records.delete()
                    print(f"✅ {count} '{status}' жазуу өчүрүлдү")
                else:
                    print("❌ Операция жокко чыгарылды")
            else:
                print(f"ℹ️  '{status}' жазуулар жок")
        else:
            print("❌ Туура эмес тандоо")
    
    elif choice == "4":
        # Бардыгын өчүрүү
        total = Attendance.objects.count()
        if total > 0:
            confirm = input(f"⚠️  БАРДЫК {total} attendance жазууну өчүрөсүзбү? (yes/no): ")
            if confirm.lower() in ['yes', 'y', 'ооба']:
                Attendance.objects.all().delete()
                print(f"✅ Бардык {total} жазуу өчүрүлдү")
            else:
                print("❌ Операция жокко чыгарылды")
        else:
            print("ℹ️  База бош")
    
    elif choice == "5":
        # Статистика
        show_statistics()
    
    else:
        print("❌ Туура эмес тандоо")

def show_statistics():
    total = Attendance.objects.count()
    present = Attendance.objects.filter(status='Present').count()
    absent = Attendance.objects.filter(status='Absent').count()
    late = Attendance.objects.filter(status='Late').count()
    excused = Attendance.objects.filter(status='Excused').count()
    
    print("\n📊 УЧУРДАГЫ ATTENDANCE СТАТИСТИКАСЫ:")
    print("-" * 50)
    print(f"📝 Жалпы жазуулар: {total}")
    print(f"✅ Катышты (Present): {present}")
    print(f"❌ Катышкан жок (Absent): {absent}")
    print(f"⏰ Кечикти (Late): {late}")
    print(f"📋 Уруксат менен жок (Excused): {excused}")
    
    if total > 0:
        print(f"\n📈 ПАЙЫЗДАР:")
        print(f"✅ Present: {round(present/total*100, 1)}%")
        print(f"❌ Absent: {round(absent/total*100, 1)}%")
        print(f"⏰ Late: {round(late/total*100, 1)}%")
        print(f"📋 Excused: {round(excused/total*100, 1)}%")

if __name__ == '__main__':
    clean_attendance_data()