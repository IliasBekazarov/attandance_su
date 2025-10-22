#!/usr/bin/env python
"""
Ата-энелердин санын текшерүү жана оңдоо
"""

import os
import django
import sys

# Django орнотуу
sys.path.append('/Users/k_beknazarovicloud.com/Downloads/su_attendance-main 2')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance_system.settings')
django.setup()

from core.models import UserProfile

print("🔍 Ата-энелердин санын текшерүү...")

parents = UserProfile.objects.filter(role='PARENT')
print(f"📊 Ата-энелер: {parents.count()}")

for parent in parents[:5]:
    print(f"  - {parent.user.get_full_name()} ({parent.user.username})")
    print(f"    Балдары: {parent.students.count()}")

print(f"\n✅ Жалпы ата-энелер: {parents.count()}")
