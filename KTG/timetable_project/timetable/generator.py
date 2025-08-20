import random
from collections import defaultdict
from .models import SchoolClass, SubjectAllocation, Teacher, TimeSlot, Lesson

class TimetableGenerator:
    def __init__(self, school_classes):
        self.school_classes = school_classes
        self.time_slots = list(TimeSlot.objects.filter(is_break=False).order_by('day', 'start_time'))
        self.teachers = list(Teacher.objects.all())
        self.lessons_to_schedule = []
        self.timetable = defaultdict(lambda: defaultdict(lambda: None))  # timetable[class][slot]

    def prepare_lessons(self):
        """Create a list of lessons to schedule."""
        Lesson.objects.all().delete()
        for s_class in self.school_classes:
            allocations = SubjectAllocation.objects.filter(school_class=s_class)
            for alloc in allocations:
                total = alloc.lessons_per_week
                if alloc.requires_double_period:
                    for _ in range(total // 2):
                        self.lessons_to_schedule.append({'class': s_class, 'alloc': alloc, 'is_double': True})
                    if total % 2 == 1:
                        self.lessons_to_schedule.append({'class': s_class, 'alloc': alloc, 'is_double': False})
                else:
                    for _ in range(total):
                        self.lessons_to_schedule.append({'class': s_class, 'alloc': alloc, 'is_double': False})
        random.shuffle(self.lessons_to_schedule)

    def is_class_free(self, s_class, slot):
        return self.timetable[s_class.id][slot.id] is None

    def is_teacher_free(self, teacher, slot):
        return not Lesson.objects.filter(teacher=teacher, time_slot=slot).exists()

    def find_teacher(self, alloc, slot):
        candidates = list(Teacher.objects.filter(subjects=alloc.subject))
        random.shuffle(candidates)
        for teacher in candidates:
            weekly = Lesson.objects.filter(teacher=teacher).count()
            daily = Lesson.objects.filter(teacher=teacher, time_slot__day=slot.day).count()
            if teacher.max_lessons_per_week > weekly and \
               teacher.max_lessons_per_day > daily and \
               self.is_teacher_free(teacher, slot):
                return teacher
        print(f"No teacher available for {alloc.subject.name} at {slot}")
        return None

    def get_next_consecutive_slot(self, slot):
        next_slot = TimeSlot.objects.filter(
            day=slot.day,
            start_time=slot.end_time,
            is_break=False
        ).first()
        if not next_slot:
            print(f"No next slot after {slot}")
        return next_slot

    def generate(self):
        self.prepare_lessons()
        skipped = []

        print(f"Preparing to schedule {len(self.lessons_to_schedule)} lessons")

        for lesson_info in self.lessons_to_schedule:
            s_class = lesson_info['class']
            alloc = lesson_info['alloc']
            is_double = lesson_info['is_double']

            placed = False
            for slot in self.time_slots:
                if not self.is_class_free(s_class, slot):
                    print(f"{s_class.name} is not free at {slot}")
                    continue

                teacher = self.find_teacher(alloc, slot)
                if not teacher:
                    print(f"No teacher found for {alloc.subject.name} at {slot} in {s_class.name}")
                    continue

                if is_double:
                    next_slot = self.get_next_consecutive_slot(slot)
                    if not next_slot or \
                       not self.is_class_free(s_class, next_slot) or \
                       not self.is_teacher_free(teacher, next_slot):
                        print(f"Double lesson slot not available for {alloc.subject.name} in {s_class.name}, trying single")
                        is_double = False  # fallback to single

                if is_double:
                    Lesson.objects.create(subject_allocation=alloc, teacher=teacher, time_slot=slot, school_class=s_class)
                    Lesson.objects.create(subject_allocation=alloc, teacher=teacher, time_slot=next_slot, school_class=s_class)
                    self.timetable[s_class.id][slot.id] = alloc.subject.name
                    self.timetable[s_class.id][next_slot.id] = alloc.subject.name
                else:
                    Lesson.objects.create(subject_allocation=alloc, teacher=teacher, time_slot=slot, school_class=s_class)
                    self.timetable[s_class.id][slot.id] = alloc.subject.name

                placed = True
                break

            if not placed:
                skipped.append((s_class.name, alloc.subject.name, is_double))

        if skipped:
            print("\n⚠️ Some lessons could not be scheduled:")
            for info in skipped:
                print(f" - {info[1]} for {info[0]} ({'Double' if info[2] else 'Single'})")

        return True if not skipped else False
