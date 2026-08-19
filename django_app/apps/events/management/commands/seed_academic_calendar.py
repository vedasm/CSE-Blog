import datetime
from django.core.management.base import BaseCommand
from apps.events.models import Event, ScheduleItem


class Command(BaseCommand):
    help = 'Seeds sample predefined academic calendar dates and department events for SRM Valliammai CSE.'

    def handle(self, *args, **options):
        today = datetime.date.today()
        year = today.year
        month = today.month

        # Sample Predefined Academic & Department Schedules
        sample_schedules = [
            {
                'title': 'Internal Assessment Test 1 (IAT-1)',
                'category': ScheduleItem.Category.EXAM,
                'start_date': datetime.date(year, month, max(1, min(28, today.day + 2))),
                'end_date': datetime.date(year, month, max(1, min(28, today.day + 6))),
                'start_time': datetime.time(9, 30),
                'end_time': datetime.time(12, 30),
                'venue': 'CSE Examination Halls (Rooms 201 - 208)',
                'description': 'IAT-1 for 2nd, 3rd, and 4th year CSE students. Syllabus: Units 1 & 2.',
                'is_academic_calendar': True,
                'is_published': True,
            },
            {
                'title': 'Smart India Hackathon 2026 - Department Screening',
                'category': ScheduleItem.Category.HACKATHON,
                'start_date': datetime.date(year, month, max(1, min(28, today.day + 5))),
                'end_date': None,
                'start_time': datetime.time(10, 0),
                'end_time': datetime.time(17, 0),
                'venue': 'CSE Advanced Computing Lab & Seminar Hall',
                'description': 'Internal hackathon screening round for SIH 2026 team idea submissions.',
                'registration_link': 'https://hackathon.valliammai.ac.in',
                'is_academic_calendar': False,
                'is_published': True,
            },
            {
                'title': 'Hands-on Workshop: Deep Learning with PyTorch & GenAI',
                'category': ScheduleItem.Category.WORKSHOP,
                'start_date': datetime.date(year, month, max(1, min(28, today.day + 8))),
                'end_date': None,
                'start_time': datetime.time(13, 30),
                'end_time': datetime.time(16, 30),
                'venue': 'CSE Cloud & AI Laboratory',
                'description': 'Hands-on session on Transformer architectures and fine-tuning open models.',
                'registration_link': 'https://workshop.valliammai.ac.in',
                'is_academic_calendar': False,
                'is_published': True,
            },
            {
                'title': 'Zoho On-Campus Placement Drive',
                'category': ScheduleItem.Category.PLACEMENT,
                'start_date': datetime.date(year, month, max(1, min(28, today.day + 12))),
                'end_date': datetime.date(year, month, max(1, min(28, today.day + 13))),
                'start_time': datetime.time(8, 30),
                'end_time': datetime.time(18, 0),
                'venue': 'Main Placement Auditorium',
                'description': 'Zoho Corporation campus recruitment drive for 2026 graduating batch.',
                'is_academic_calendar': True,
                'is_published': True,
            },
            {
                'title': 'Project Phase-1 Review (Final Year B.E CSE)',
                'category': ScheduleItem.Category.ACADEMIC,
                'start_date': datetime.date(year, month, max(1, min(28, today.day + 15))),
                'end_date': None,
                'start_time': datetime.time(9, 0),
                'end_time': datetime.time(16, 0),
                'venue': 'CSE Project Labs',
                'description': 'Zero review & Phase-1 architecture presentation before department panel.',
                'is_academic_calendar': True,
                'is_published': True,
            },
            {
                'title': 'Internal Assessment Test 2 (IAT-2)',
                'category': ScheduleItem.Category.EXAM,
                'start_date': datetime.date(year, month, max(1, min(28, today.day + 18))),
                'end_date': datetime.date(year, month, max(1, min(28, today.day + 22))),
                'start_time': datetime.time(9, 30),
                'end_time': datetime.time(12, 30),
                'venue': 'CSE Examination Halls',
                'description': 'IAT-2 for all semesters. Syllabus: Units 3 & 4.',
                'is_academic_calendar': True,
                'is_published': True,
            },
        ]

        count = 0
        for item_data in sample_schedules:
            obj, created = ScheduleItem.objects.update_or_create(
                title=item_data['title'],
                defaults=item_data
            )
            if created:
                count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {count} sample academic calendar schedules.'))
