#!/usr/bin/env python
"""
TimeSlot'тарды түзүү (сабак убакыттары)
"""

import os
import django
import sys
from datetime import time

# Django орнотуу
sys.path.append('/Users/k_beknazarovicloud.com/Downloads/su_attendance-main 2')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance_system.settings')
django.setup()

from core.models import TimeSlot

print("⏰ TimeSlot'тарды түзүү...")

# TimeSlot'тардын тизмеси
time_slots_data = [
    {'name': '1-пара', 'start': time(8, 0), 'end': time(9, 30), 'order': 1},
    {'name': '2-пара', 'start': time(9, 40), 'end': time(11, 10), 'order': 2},
    {'name': '3-пара', 'start': time(11, 20), 'end': time(12, 50), 'order': 3},
    {'name': '4-пара', 'start': time(14, 0), 'end': time(15, 30), 'order': 4},
    {'name': '5-пара', 'start': time(15, 40), 'end': time(17, 10), 'order': 5},
    {'name': '6-пара', 'start': time(17, 20), 'end': time(18, 50), 'order': 6},
]

created_count = 0

for slot_data in time_slots_data:
    slot, created = TimeSlot.objects.get_or_create(
        name=slot_data['name'],
        defaults={
            'start_time': slot_data['start'],
            'end_time': slot_data['end'],
            'order': slot_data['order'],
            'is_active': True
        }
    )
    
    if created:
        created_count += 1
        print(f"  ✅ {slot.name}: {slot.start_time.strftime('%H:%M')} - {slot.end_time.strftime('%H:%M')}")

print(f"\n✅ {created_count} TimeSlot түзүлдү")
print(f"📊 Жалпы TimeSlot'тар: {TimeSlot.objects.count()}")