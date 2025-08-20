import africastalking
from django.utils import timezone
from datetime import timedelta
from .models import Lesson

# 🔐 Replace these with your credentials
username = "sandbox"  # Always 'sandbox' while testing
api_key = "atsk_ef5ee3e70f4feb7a26d1cce0dc5b9ee9d2c9ab0ac6efab9b4e160c32bc064bceae42360c"

africastalking.initialize(username, api_key)
sms = africastalking.SMS

def send_upcoming_lesson_alerts():
    now = timezone.localtime().time()
    upcoming = (timezone.localtime() + timedelta(minutes=10)).time()
    today = timezone.localtime().strftime('%A')

    lessons = Lesson.objects.filter(
        time_slot__day=today,
        time_slot__start_time__gte=now,
        time_slot__start_time__lte=upcoming
    )

    for lesson in lessons:
        teacher = lesson.teacher
        if teacher.phone_number:
            message = f"Reminder: You have {lesson.subject_allocation.subject.name} with {lesson.school_class.name} at {lesson.time_slot.start_time.strftime('%H:%M')}."
            try:
                sms.send(message, [teacher.phone_number])
                print(f"✅ Sent to {teacher.name}: {teacher.phone_number}")
            except Exception as e:
                print(f"❌ Failed to send to {teacher.name}: {e}")
