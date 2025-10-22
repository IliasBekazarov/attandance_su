#!/usr/bin/env python
"""
Attendance маалыматтарын тазалоо скрипти
Бардык "Absent", "Late", "Excused" жазууларын өчүрөт
"""

import os
import django
import sys

# Django орнотуу
sys.path.append('/Users/k_beknazarovicloud.com/Downloads/su_attendance-main 2')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance_system.settings')
django.setup()

from core.models import Attendance

print("⚠️  ATTENDANCE МААЛЫМАТТАРЫН ТАЗАЛОО")
print("=" * 60)

# Учурдагы attendance статистикасы
total_records = Attendance.objects.count()
present_records = Attendance.objects.filter(status='Present').count()
absent_records = Attendance.objects.filter(status='Absent').count()
late_records = Attendance.objects.filter(status='Late').count()
excused_records = Attendance.objects.filter(status='Excused').count()

print("📊 УЧУРДАГЫ СТАТИСТИКА:")
print(f"  📝 Жалпы жазуулар: {total_records}")
print(f"  ✅ Катышты (Present): {present_records}")
print(f"  ❌ Катышкан жок (Absent): {absent_records}")
print(f"  ⏰ Кечикти (Late): {late_records}")
print(f"  📋 Уруксат менен жок (Excused): {excused_records}")

print("\n🗑️  ТАЗАЛОО ПРОЦЕССИ:")

# Present болбогон бардык жазууларды өчүрүү
non_present_records = Attendance.objects.exclude(status='Present')
deleted_count = non_present_records.count()

if deleted_count > 0:
    # Жазууларды өчүрүү
    non_present_records.delete()
    print(f"  ✅ {deleted_count} жазуу өчүрүлдү")
    print(f"     - Absent: {absent_records}")
    print(f"     - Late: {late_records}")
    print(f"     - Excused: {excused_records}")
else:
    print("  ℹ️  Өчүрүүгө жазуу жок")

# Жаңы статистика
new_total = Attendance.objects.count()
new_present = Attendance.objects.filter(status='Present').count()

print("\n📊 ЖАҢЫ СТАТИСТИКА:")
print(f"  📝 Жалпы жазуулар: {new_total}")
print(f"  ✅ Катышты (Present): {new_present}")
print(f"  ❌ Катышкан жок (Absent): {Attendance.objects.filter(status='Absent').count()}")
print(f"  ⏰ Кечикти (Late): {Attendance.objects.filter(status='Late').count()}")
print(f"  📋 Уруксат менен жок (Excused): {Attendance.objects.filter(status='Excused').count()}")

print("\n" + "=" * 60)
print("✨ ТАЗАЛОО АЯКТАДЫ!")
print("Эми сиз бүгүндөн баштап кол менен attendance киргизе аласыз.")
print("=" * 60)