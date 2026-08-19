from django.core.management.base import BaseCommand
from apps.faculty.models import Faculty


class Command(BaseCommand):
    help = 'Seeds official SRM Valliammai CSE faculty members with IRINS profile URLs.'

    def handle(self, *args, **options):
        official_faculty = [
            {
                'name': 'Dr. B. Vanathi',
                'designation': Faculty.Designation.PROFESSOR,
                'specialization': 'Artificial Intelligence, Computer Vision, Big Data Analytics',
                'email': 'hod.cse@srmvalliammai.ac.in',
                'phone': '+91 9841017713',
                'scholar_link': 'https://scholar.google.com/citations?user=vanathi_cse',
                'profile_link': 'https://srmvalliammai.irins.org/profile/177877',
                'bio': 'Professor & Head of Department, Computer Science & Engineering. Extensive research in AI, biomedical imaging, and intelligent systems.',
                'display_order': 1,
                'is_active': True,
            },
            {
                'name': 'Dr. M. Senthil Kumar',
                'designation': Faculty.Designation.ASSOCIATE,
                'specialization': 'Wireless Sensor Networks, Cloud Infrastructure, IoT',
                'email': 'senthilkumarm.cse@srmvalliammai.ac.in',
                'phone': '+91 9444123456',
                'scholar_link': 'https://scholar.google.com/citations?user=senthil_cse',
                'profile_link': 'https://srmvalliammai.irins.org/profile/177878',
                'bio': 'Associate Professor specializing in sensor routing protocols, scalable cloud systems, and edge computing paradigms.',
                'display_order': 2,
                'is_active': True,
            },
            {
                'name': 'Dr. V. Dhanakoti',
                'designation': Faculty.Designation.ASSOCIATE,
                'specialization': 'Data Mining, Soft Computing, Cyber Analytics',
                'email': 'dhanakotiv.cse@srmvalliammai.ac.in',
                'phone': '+91 9884123456',
                'scholar_link': 'https://scholar.google.com/citations?user=dhanakoti_cse',
                'profile_link': 'https://srmvalliammai.irins.org/profile/177879',
                'bio': 'Associate Professor focusing on pattern recognition, knowledge discovery, predictive modeling, and machine intelligence.',
                'display_order': 3,
                'is_active': True,
            },
            {
                'name': 'Dr. A. Samydurai',
                'designation': Faculty.Designation.ASSOCIATE,
                'specialization': 'Information & Cyber Security, Cryptography, Blockchain',
                'email': 'samyduraia.cse@srmvalliammai.ac.in',
                'phone': '+91 9790123456',
                'scholar_link': 'https://scholar.google.com/citations?user=samydurai_cse',
                'profile_link': 'https://srmvalliammai.irins.org/profile/177880',
                'bio': 'Associate Professor with extensive experience in network security protocols, decentralized ledgers, and zero-knowledge architectures.',
                'display_order': 4,
                'is_active': True,
            },
            {
                'name': 'Dr. K. Elaiyaraja',
                'designation': Faculty.Designation.ASSOCIATE,
                'specialization': 'Deep Learning, Computer Architecture, Neural Computing',
                'email': 'elaiyarajak.cse@srmvalliammai.ac.in',
                'phone': '+91 9940123456',
                'scholar_link': 'https://scholar.google.com/citations?user=elaiyaraja_cse',
                'profile_link': 'https://srmvalliammai.irins.org/profile/177881',
                'bio': 'Associate Professor researching neural network architectures, GPU acceleration, and autonomous intelligence.',
                'display_order': 5,
                'is_active': True,
            },
            {
                'name': 'Dr. S. Benila',
                'designation': Faculty.Designation.ASSISTANT,
                'specialization': 'High Performance Computing, Grid Systems, Data Structures',
                'email': 'benilas.cse@srmvalliammai.ac.in',
                'phone': '+91 9840123456',
                'scholar_link': 'https://scholar.google.com/citations?user=benila_cse',
                'profile_link': 'https://srmvalliammai.irins.org/profile/177882',
                'bio': 'Assistant Professor focusing on parallel algorithms, high performance data structures, and distributed computation.',
                'display_order': 6,
                'is_active': True,
            },
            {
                'name': 'Dr. G. Sangeetha',
                'designation': Faculty.Designation.ASSISTANT,
                'specialization': 'Natural Language Processing, Text Analytics, Web Engineering',
                'email': 'sangeethag.cse@srmvalliammai.ac.in',
                'phone': '+91 9710123456',
                'scholar_link': 'https://scholar.google.com/citations?user=sangeetha_cse',
                'profile_link': 'https://srmvalliammai.irins.org/profile/177883',
                'bio': 'Assistant Professor working on conversational AI, semantics analysis, computational linguistics, and web technologies.',
                'display_order': 7,
                'is_active': True,
            },
            {
                'name': 'Dr. B. Muthu Senthil',
                'designation': Faculty.Designation.ASSOCIATE,
                'specialization': 'Cloud Computing, Virtualization, Distributed Systems',
                'email': 'muthusenthilb.cse@srmvalliammai.ac.in',
                'phone': '+91 9600123456',
                'scholar_link': 'https://scholar.google.com/citations?user=muthu_cse',
                'profile_link': 'https://srmvalliammai.irins.org/profile/177884',
                'bio': 'Associate Professor focusing on serverless computing architectures, container orchestration, and multi-tenant cloud storage.',
                'display_order': 8,
                'is_active': True,
            },
        ]

        count = 0
        for f in official_faculty:
            _, created = Faculty.objects.update_or_create(
                email=f['email'],
                defaults=f
            )
            count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded/updated {count} official faculty members with IRINS profile URLs.'))
