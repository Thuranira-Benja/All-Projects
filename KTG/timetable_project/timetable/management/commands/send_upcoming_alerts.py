from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from timetable.models import Lesson
import africastalking

class Command(BaseCommand):
    help = "Send SMS alerts to teachers for upcoming lessons within the next 10 minutes."

    def handle(self, *args, **kwargs):
        # Initialize Africa's Talking
        username = "sandbox"
        api_key = "atsk_ef5ee3e70f4feb7a26d1cce0dc5b9ee9d2c9ab0ac6efab9b4e160c32bc064bceae42360c"
        africastalking.initialize(username, api_key)
        sms = africastalking.SMS

        # Get current time and time 10 mins from now
        now = timezone.localtime()
        in_10_min = now + timedelta(minutes=10)

        today = now.strftime('%A')
        now_time = now.time()
        future_time = in_10_min.time()

        # Filter lessons starting within the next 10 minutes
        lessons = Lesson.objects.filter(
            time_slot__day=today,
            time_slot__start_time__gte=now_time,
            time_slot__start_time__lte=future_time
        )

        for lesson in lessons:
            teacher = lesson.teacher
            phone = teacher.phone_number
            if not phone:
                self.stdout.write(self.style.WARNING(f"No phone number for {teacher.name}"))
                continue

            message = f"Reminder: {lesson.subject_allocation.subject.name} with {lesson.school_class.name} at {lesson.time_slot.start_time.strftime('%H:%M')} today."

            try:
                sms.send(message, [phone])
                self.stdout.write(self.style.SUCCESS(f"✅ Sent to {teacher.name}: {phone}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"❌ Failed to send to {teacher.name}: {e}"))
