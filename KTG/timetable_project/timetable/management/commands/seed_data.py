# timetable/management/commands/seed_data.py

from django.core.management.base import BaseCommand
from timetable.models import *
import datetime

class Command(BaseCommand):
    help = 'Seeds the database with initial data for flexible timetable testing'

    def handle(self, *args, **options):
        self.stdout.write('🔄 Deleting old data...')
        Lesson.objects.all().delete()
        SubjectAllocation.objects.all().delete()
        Teacher.objects.all().delete()
        Subject.objects.all().delete()
        SchoolClass.objects.all().delete()
        System.objects.all().delete()
        TimeSlot.objects.all().delete()

        self.stdout.write('✅ Creating base data...')

        # Systems
        system_844 = System.objects.create(name='8-4-4')

        # Classes
        form1 = SchoolClass.objects.create(system=system_844, name='Form 1')
        form2 = SchoolClass.objects.create(system=system_844, name='Form 2')

        # Subjects
        math = Subject.objects.create(name='Mathematics')
        eng = Subject.objects.create(name='English')
        kis = Subject.objects.create(name='Kiswahili')
        chem = Subject.objects.create(name='Chemistry')

        # Teachers
        teacher_john = Teacher.objects.create(name='Mr. John', max_lessons_per_week=20)
        teacher_jane = Teacher.objects.create(name='Ms. Jane', max_lessons_per_week=18)
        teacher_peter = Teacher.objects.create(name='Mr. Peter', max_lessons_per_week=22)

        teacher_john.subjects.add(math, chem)
        teacher_jane.subjects.add(eng, kis)
        teacher_peter.subjects.add(math, eng)

        # Subject Allocations
        SubjectAllocation.objects.create(school_class=form1, subject=math, lessons_per_week=5)
        SubjectAllocation.objects.create(school_class=form1, subject=eng, lessons_per_week=5)
        SubjectAllocation.objects.create(school_class=form1, subject=kis, lessons_per_week=4)
        SubjectAllocation.objects.create(school_class=form1, subject=chem, lessons_per_week=3, requires_double_period=True)

        SubjectAllocation.objects.create(school_class=form2, subject=math, lessons_per_week=5)
        SubjectAllocation.objects.create(school_class=form2, subject=eng, lessons_per_week=4)
        SubjectAllocation.objects.create(school_class=form2, subject=kis, lessons_per_week=4)
        SubjectAllocation.objects.create(school_class=form2, subject=chem, lessons_per_week=4, requires_double_period=True)

        # Time Slots (flexible durations with short + long breaks)
        self.stdout.write('⏱ Generating flexible time slots...')
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        flexible_structure = [
            (40, False),  # Lesson 1
            (40, False),  # Lesson 2
            (15, True),   # Tea Break
            (40, False),  # Lesson 3
            (40, False),  # Lesson 4
            (60, True),   # Lunch Break
            (40, False),  # Lesson 5
            (40, False),  # Lesson 6
        ]

        for day in days:
            current = datetime.datetime.combine(datetime.date.today(), datetime.time(8, 0))  # Start at 8:00 AM
            for duration, is_break in flexible_structure:
                start_time = current.time()
                current += datetime.timedelta(minutes=duration)
                end_time = current.time()
                TimeSlot.objects.create(
                    day=day,
                    start_time=start_time,
                    end_time=end_time,
                    is_break=is_break
                )

        self.stdout.write(self.style.SUCCESS('✅ Successfully seeded the database with flexible timetable slots.'))
