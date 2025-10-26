from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserProfile, Student, Course, Group, Teacher, Attendance, Notification, Subject, LeaveRequest
from datetime import timedelta

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Жаңы колдонуучу катталганда автоматтык түрдө профил түзүү"""
    if created:
        profile = UserProfile.objects.create(user=instance, role='STUDENT')
        # Профилдин толуктугун текшерүү
        profile.check_profile_completeness()

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """User сакталганда профилди да сактоо"""
    try:
        instance.userprofile.save()
    except UserProfile.DoesNotExist:
        # Эгер профил жок болсо, жаңысын түзүү
        UserProfile.objects.create(user=instance, role='STUDENT')

@receiver(post_save, sender=UserProfile)
def create_student_or_teacher(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'STUDENT':
            default_course = Course.objects.first() or Course.objects.create(name='1st Year', year=1)
            default_group = Group.objects.first() or Group.objects.create(name='A-Group', course=default_course)
            Student.objects.create(
                user=instance.user,
                name=instance.user.get_full_name() or instance.user.username,
                course=default_course,
                group=default_group
            )
        elif instance.role == 'TEACHER':
            Teacher.objects.create(
                user=instance.user,
                name=instance.user.get_full_name() or instance.user.username
            )
            
@receiver(post_save, sender=Attendance)
def create_absent_notification(sender, instance, created, **kwargs):
    if created and instance.status == 'Absent':
        teacher = instance.subject.teacher
        if teacher and teacher.user:
            Notification.objects.create(
                recipient=teacher.user,
                notification_type='ABSENCE',
                title='Студент катышкан жок',
                message=f"{instance.student.name} {instance.subject.subject_name} сабагына катышкан жок ({instance.date}).",
                student=instance.student
            )

@receiver(post_save, sender=LeaveRequest)
def handle_leave_request_approval(sender, instance, **kwargs):
    """
    Leave Request APPROVED болгондо автоматтык Excused attendance түзүү
    """
    # Эгер approved болсо жана мурда attendance түзүлбөгөн болсо
    if instance.status == 'APPROVED':
        from .models import Schedule
        
        # Start date дан end date га чейинки бардык күндөр
        current_date = instance.start_date
        while current_date <= instance.end_date:
            # Күндүн английс атын табуу
            weekday_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            day_name = weekday_names[current_date.weekday()]
            
            # Студенттин группасы боюнча ошол күндөгү сабактар
            schedules = Schedule.objects.filter(
                group=instance.student.group,
                day=day_name,
                is_active=True
            )
            
            for schedule in schedules:
                try:
                    # Алгач attendance бар болсо текшерүү
                    existing_attendance = Attendance.objects.filter(
                        student=instance.student,
                        subject=schedule.subject,
                        date=current_date
                    ).first()
                    
                    if existing_attendance:
                        # Эгер дагы деле бар болсо, Excused кылуу
                        existing_attendance.status = 'Excused'
                        existing_attendance.leave_request = instance
                        existing_attendance.save()
                    else:
                        # Жаңы attendance түзүү
                        Attendance.objects.create(
                            student=instance.student,
                            subject=schedule.subject,
                            schedule=schedule,
                            date=current_date,
                            status='Excused',
                            created_by=instance.approved_by,
                            student_name=instance.student.name,
                            subject_name=schedule.subject.subject_name,
                            leave_request=instance,
                            is_active=True
                        )
                except Exception as e:
                    # Ката болсо, лог жазып өтүү
                    print(f"Error creating attendance: {e}")
                    continue
            
            # Кийинки күнгө өтүү
            current_date += timedelta(days=1)
        
        # Студентке notification жөнөтүү
        if instance.student.user:
            try:
                Notification.objects.create(
                    recipient=instance.student.user,
                    notification_type='LEAVE_APPROVED',
                    title='Бошотуу сурамы бекитилди',
                    message=f"Сиздин {instance.start_date} - {instance.end_date} аралыгындагы бошотуу сурамыңыз бекитилди.",
                    student=instance.student,
                    leave_request=instance
                )
            except Exception as e:
                print(f"Error creating notification: {e}")