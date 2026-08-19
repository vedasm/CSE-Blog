from datetime import datetime, timedelta
from io import BytesIO

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.utils.text import slugify
from PIL import Image, ImageDraw

from apps.accounts.models import AdminUser
from apps.blog.models import Blog, Category
from apps.events.models import Event
from apps.faculty.models import Faculty
from apps.gallery.models import GalleryImage


def image_file(label, colour, filename):
    canvas = Image.new('RGB', (1200, 700), colour)
    draw = ImageDraw.Draw(canvas)
    draw.text((60, 60), label, fill='white')
    data = BytesIO()
    canvas.save(data, format='JPEG', quality=88)
    return ContentFile(data.getvalue(), name=filename)


class Command(BaseCommand):
    help = 'Creates idempotent sample content for local development.'

    def handle(self, *args, **options):
        try:
            admin = AdminUser.objects.get(email='admin@srmvec.in')
        except AdminUser.DoesNotExist as exc:
            raise CommandError('Create admin@srmvec.in before seeding sample data.') from exc

        categories = {}
        for name in ('Artificial Intelligence', 'Cyber Security', 'Cloud Computing'):
            categories[name], _ = Category.objects.get_or_create(name=name)

        blogs = [
            ('AI in Education: Building Better Learning Experiences', 'Artificial Intelligence', 'AI, education, innovation', '#0066cc'),
            ('Cyber Security Essentials for Engineering Students', 'Cyber Security', 'security, privacy, networks', '#a12c2c'),
            ('Cloud Computing for Modern Application Development', 'Cloud Computing', 'cloud, DevOps, deployment', '#5d3ea8'),
        ]
        for title, category, tags, colour in blogs:
            blog, created = Blog.objects.get_or_create(
                slug=slugify(title)[:50],
                defaults={
                    'title': title, 'author': admin, 'category': categories[category],
                    'content': f'<h2>{title}</h2><p>This sample article introduces practical concepts, current applications, and useful next steps for CSE students.</p>',
                    'tags': tags, 'status': 'published', 'published_at': timezone.now(),
                },
            )
            if created:
                blog.featured_image.save(f'{blog.slug}.jpg', image_file(title, colour, f'{blog.slug}.jpg'), save=True)

        events = [
            ('AI Innovation Workshop', 'workshop', 14, 'CSE Seminar Hall', '#1565c0'),
            ('CodeSprint 2026', 'hackathon', 28, 'Main Auditorium', '#388e3c'),
            ('Industry Talk: Secure Systems', 'guest_lecture', 42, 'CSE Block A', '#ef6c00'),
        ]
        for title, category, days, venue, colour in events:
            event, created = Event.objects.get_or_create(
                title=title,
                defaults={'category': category, 'event_date': timezone.localdate() + timedelta(days=days), 'event_time': datetime.strptime('10:00', '%H:%M').time(), 'venue': venue, 'description': f'Join us for {title}, featuring hands-on learning and expert guidance.', 'status': 'upcoming'},
            )
            if created:
                event.image.save(f'{title.lower().replace(" ", "-")}.jpg', image_file(title, colour, 'event.jpg'), save=True)

        faculty = [
            ('Dr. Anitha Raj', 'professor', 'Artificial Intelligence and Machine Learning', 'anitha.raj@srmvec.in', '#3f51b5'),
            ('Dr. Karthik Kumar', 'associate_professor', 'Cloud Computing and Distributed Systems', 'karthik.kumar@srmvec.in', '#00897b'),
            ('Ms. Priya S', 'assistant_professor', 'Cyber Security and Computer Networks', 'priya.s@srmvec.in', '#c62828'),
        ]
        for index, (name, designation, specialization, email, colour) in enumerate(faculty, 1):
            member, created = Faculty.objects.get_or_create(
                email=email,
                defaults={'name': name, 'designation': designation, 'specialization': specialization, 'phone': '9000000000', 'bio': f'{name} is a sample faculty profile for the CSE department.', 'display_order': index, 'is_active': True},
            )
            if created:
                member.photo.save(f'{name.lower().replace(" ", "-")}.jpg', image_file(name, colour, 'faculty.jpg'), save=True)

        for title, category, colour in [('AI Workshop', 'Workshop', '#1565c0'), ('CodeSprint 2026', 'Hackathon', '#388e3c'), ('Research Seminar', 'Seminar', '#7b1fa2'), ('Placement Drive', 'Placements', '#ef6c00')]:
            if not GalleryImage.objects.filter(title=title, category=category).exists():
                item = GalleryImage(title=title, category=category, uploaded_by=admin)
                item.image.save(f'{title.lower().replace(" ", "-")}.jpg', image_file(title, colour, 'gallery.jpg'), save=True)

        self.stdout.write(self.style.SUCCESS('Sample data is ready.'))
