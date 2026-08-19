from django.core.management.base import BaseCommand
from apps.core.models import DepartmentDocument, PlacementStat, DepartmentLab, DepartmentMilestone


class Command(BaseCommand):
    help = 'Seeds official SRM Valliammai CSE department documents, placement records, labs, and milestones.'

    def handle(self, *args, **options):
        # 1. Placement Records (2015 - 2023)
        placements_data = [
            {'year': 2023, 'students_placed': 149, 'total_offers': 165, 'highest_package': '12 LPA', 'average_package': '4.5 LPA', 'top_recruiters': 'TCS, CTS, Wipro, Infosys, Zoho, Accenture, HCL, Cognizant'},
            {'year': 2022, 'students_placed': 114, 'total_offers': 130, 'highest_package': '10 LPA', 'average_package': '4.2 LPA', 'top_recruiters': 'TCS, CTS, Wipro, Infosys, Zoho, Accenture, HCL'},
            {'year': 2021, 'students_placed': 143, 'total_offers': 155, 'highest_package': '9.5 LPA', 'average_package': '4.0 LPA', 'top_recruiters': 'TCS, CTS, Wipro, Infosys, Accenture, HCL, Mindtree'},
            {'year': 2020, 'students_placed': 83, 'total_offers': 92, 'highest_package': '8 LPA', 'average_package': '3.8 LPA', 'top_recruiters': 'TCS, CTS, Wipro, Infosys, HCL, DXC'},
            {'year': 2019, 'students_placed': 53, 'total_offers': 60, 'highest_package': '7.5 LPA', 'average_package': '3.6 LPA', 'top_recruiters': 'TCS, CTS, Wipro, Infosys, Tech Mahindra'},
            {'year': 2018, 'students_placed': 53, 'total_offers': 58, 'highest_package': '7 LPA', 'average_package': '3.5 LPA', 'top_recruiters': 'TCS, CTS, Wipro, Infosys, Capgemini'},
            {'year': 2017, 'students_placed': 66, 'total_offers': 72, 'highest_package': '6.5 LPA', 'average_package': '3.4 LPA', 'top_recruiters': 'TCS, CTS, Wipro, Infosys'},
            {'year': 2016, 'students_placed': 68, 'total_offers': 75, 'highest_package': '6 LPA', 'average_package': '3.2 LPA', 'top_recruiters': 'TCS, CTS, Wipro, Infosys'},
            {'year': 2015, 'students_placed': 48, 'total_offers': 52, 'highest_package': '5.5 LPA', 'average_package': '3.0 LPA', 'top_recruiters': 'TCS, CTS, Wipro, Infosys'},
        ]

        p_count = 0
        for p in placements_data:
            _, created = PlacementStat.objects.update_or_create(
                year=p['year'],
                defaults=p
            )
            if created:
                p_count += 1

        # 2. Official Department Documents & PDF Archives
        docs_data = [
            # Research & Journals
            {
                'title': 'Publications of Journals 2022–2023',
                'category': DepartmentDocument.Category.RESEARCH,
                'academic_year': '2022-2023',
                'description': 'Scopus, Web of Science, and Anna University listed journal publications by CSE faculty and research scholars.',
                'external_url': 'https://digitalveda.co.in/srm-valliammai/uploads/51ba570fe68fc088e0a942bdf8700cdce7eb8b1d/1775901940srm-vec-cse-list-of-journals-from-july-2022-june-2023.pdf',
                'display_order': 1,
            },
            {
                'title': 'Publications of Journals 2021–2022',
                'category': DepartmentDocument.Category.RESEARCH,
                'academic_year': '2021-2022',
                'description': 'List of peer-reviewed journal papers published during academic year July 2021 to June 2022.',
                'external_url': 'https://digitalveda.co.in/srm-valliammai/uploads/51ba570fe68fc088e0a942bdf8700cdce7eb8b1d/1775901914srm-vec-cse-list-of-journals-from-july-2021-june-2022.pdf',
                'display_order': 2,
            },
            {
                'title': 'Publications of Journals 2020–2021',
                'category': DepartmentDocument.Category.RESEARCH,
                'academic_year': '2020-2021',
                'description': 'International & National journal publications by Department of CSE.',
                'external_url': 'https://digitalveda.co.in/srm-valliammai/uploads/51ba570fe68fc088e0a942bdf8700cdce7eb8b1d/1775901874publications-journals-2018-20.pdf',
                'display_order': 3,
            },
            {
                'title': 'Publications of Journals 2018–2019',
                'category': DepartmentDocument.Category.RESEARCH,
                'academic_year': '2018-2019',
                'description': 'Research papers and conference proceedings from July 2018 to June 2019.',
                'external_url': 'https://digitalveda.co.in/srm-valliammai/uploads/51ba570fe68fc088e0a942bdf8700cdce7eb8b1d/1775901824publications-journals-july-2018-2019.pdf',
                'display_order': 4,
            },
            {
                'title': 'Anna University Recognized Research Centre Profile',
                'category': DepartmentDocument.Category.RESEARCH,
                'academic_year': 'Centre Details',
                'description': 'Anna University Chennai recognized Research Centre recognition order, recognized supervisors, and doctoral candidates.',
                'external_url': 'https://digitalveda.co.in/srm-valliammai/uploads/51ba570fe68fc088e0a942bdf8700cdce7eb8b1d/1775901721research-center-details.pdf',
                'display_order': 5,
            },

            # Achievements
            {
                'title': 'Department Achievements 2021 to 2023',
                'category': DepartmentDocument.Category.ACHIEVEMENT,
                'academic_year': '2021-2023',
                'description': 'State and National level hackathons, symposium prizes, coding victories, and faculty honors.',
                'external_url': 'https://digitalveda.co.in/srm-valliammai/uploads/51ba570fe68fc088e0a942bdf8700cdce7eb8b1d/1775898048srm-vec-cse-achievement-2021-2023.pdf',
                'display_order': 1,
            },
            {
                'title': 'Department Achievements 2018 to 2020',
                'category': DepartmentDocument.Category.ACHIEVEMENT,
                'academic_year': '2018-2020',
                'description': 'Student project awards, smart solution contests, and academic achievements.',
                'external_url': 'https://digitalveda.co.in/srm-valliammai/uploads/51ba570fe68fc088e0a942bdf8700cdce7eb8b1d/1775898025cseachievements-2017-to-dec-2021.pdf',
                'display_order': 2,
            },
            {
                'title': 'Department Achievements 2017 to 2018',
                'category': DepartmentDocument.Category.ACHIEVEMENT,
                'academic_year': '2017-2018',
                'description': 'Paper presentations, codeathons, and department awards archive.',
                'external_url': 'https://digitalveda.co.in/srm-valliammai/uploads/51ba570fe68fc088e0a942bdf8700cdce7eb8b1d/1775897992cseachievements-2017-to-2018.pdf',
                'display_order': 3,
            },

            # Events Archive
            {
                'title': 'Department Events Conducted 2020 to 2023',
                'category': DepartmentDocument.Category.EVENT_ARCHIVE,
                'academic_year': '2020-2023',
                'description': 'Workshops, international conferences, FDPs, symposiums, and guest lecture reports.',
                'external_url': 'https://digitalveda.co.in/srm-valliammai/uploads/51ba570fe68fc088e0a942bdf8700cdce7eb8b1d/1775900152srm-vec-cse-events-2020-2023.pdf',
                'display_order': 1,
            },
            {
                'title': 'Department Events Conducted 2020 to 2021',
                'category': DepartmentDocument.Category.EVENT_ARCHIVE,
                'academic_year': '2020-2021',
                'description': 'Online webinars, skill development workshops, and virtual hackathons.',
                'external_url': 'https://digitalveda.co.in/srm-valliammai/uploads/51ba570fe68fc088e0a942bdf8700cdce7eb8b1d/1775900205events2020-21-2.pdf',
                'display_order': 2,
            },
            {
                'title': 'Department Events Conducted 2018 to 2020',
                'category': DepartmentDocument.Category.EVENT_ARCHIVE,
                'academic_year': '2018-2020',
                'description': 'National symposiums, hands-on workshops, and industry interaction series.',
                'external_url': 'https://digitalveda.co.in/srm-valliammai/uploads/51ba570fe68fc088e0a942bdf8700cdce7eb8b1d/1775900235events2018-20-1.pdf',
                'display_order': 3,
            },
            {
                'title': 'Department Events Conducted 2013 to 2018',
                'category': DepartmentDocument.Category.EVENT_ARCHIVE,
                'academic_year': '2013-2018',
                'description': 'Historical record of department technical activities and conferences.',
                'external_url': 'https://digitalveda.co.in/srm-valliammai/uploads/51ba570fe68fc088e0a942bdf8700cdce7eb8b1d/1775900263events-2013-to-2019-1.pdf',
                'display_order': 4,
            },

            # Library
            {
                'title': 'Department Library Catalogue & Reference Book Index',
                'category': DepartmentDocument.Category.LIBRARY,
                'academic_year': '724 Titles',
                'description': 'Catalogue of 724 department volumes, including 112 foreign-authored reference texts across OS, Networks, AI, DBMS, and Systems.',
                'external_url': 'https://digitalveda.co.in/srm-valliammai/uploads/51ba570fe68fc088e0a942bdf8700cdce7eb8b1d/1775897175library-pdf.pdf',
                'display_order': 1,
            },

            # Alumni
            {
                'title': 'SHIMMER – Alumni Association Annual Report',
                'category': DepartmentDocument.Category.ALUMNI,
                'academic_year': 'Annual Report',
                'description': 'Annual report of SRM VEC CSE Alumni Chapter, mentorship programs, and scholarships.',
                'external_url': 'https://digitalveda.co.in/srm-valliammai/uploads/51ba570fe68fc088e0a942bdf8700cdce7eb8b1d/1775902890shimmer-annual-report.pdf',
                'display_order': 1,
            },
            {
                'title': 'Events Conducted by Alumni (2021–2022)',
                'category': DepartmentDocument.Category.ALUMNI,
                'academic_year': '2021-2022',
                'description': 'Alumni guest lectures, mock placement interviews, and technical webinars.',
                'external_url': 'https://digitalveda.co.in/srm-valliammai/uploads/51ba570fe68fc088e0a942bdf8700cdce7eb8b1d/1775902817srm-vec-cse-events-by-alumni-cse-2021-2022.pdf',
                'display_order': 2,
            },
            {
                'title': 'Events Conducted by Alumni (2020–2021)',
                'category': DepartmentDocument.Category.ALUMNI,
                'academic_year': '2020-2021',
                'description': 'Industry transition sessions and career guidance organized by CSE alumni.',
                'external_url': 'https://digitalveda.co.in/srm-valliammai/uploads/51ba570fe68fc088e0a942bdf8700cdce7eb8b1d/1775902867srm-vec-cse-events-by-alumni-cse-2020-2021.pdf',
                'display_order': 3,
            },
        ]

        d_count = 0
        for doc in docs_data:
            _, created = DepartmentDocument.objects.update_or_create(
                title=doc['title'],
                defaults=doc
            )
            if created:
                d_count += 1

        # 3. 7 Named Specialized Computing Laboratories
        labs_data = [
            {
                'name': 'James Gosling Lab (Networks & DBMS Lab)',
                'domain': 'Computer Networks, Distributed Databases & Cloud Services',
                'computers_count': 35,
                'printers_count': 3,
                'ups_info': '10 KVA Dedicated UPS Backup',
                'software_installed': 'Oracle 11g, MySQL, Visual Basic, MS Office Suite, Wireshark, Cisco Packet Tracer',
                'image_url': 'https://digitalveda.co.in/srm-valliammai/uploads/51ba570fe68fc088e0a942bdf8700cdce7eb8b1d/1775823156cse-lab-i.webp',
                'display_order': 1
            },
            {
                'name': 'Dennis Ritchie Lab (Data Structures & OOPS Lab)',
                'domain': 'Algorithms, Data Structures & Object Oriented Programming',
                'computers_count': 35,
                'printers_count': 4,
                'ups_info': '10 KVA Dedicated UPS Backup',
                'software_installed': 'GCC Compiler, Turbo C++, Java Development Kit (JDK 21), Eclipse IDE, Code::Blocks',
                'image_url': 'https://digitalveda.co.in/srm-valliammai/uploads/51ba570fe68fc088e0a942bdf8700cdce7eb8b1d/1775823169cse-lab-ii.webp',
                'display_order': 2
            },
            {
                'name': 'John Backus Lab (Operating Systems & System Software Lab)',
                'domain': 'OS Kernel Internals, Compilers & Low-Level Architecture',
                'computers_count': 35,
                'printers_count': 3,
                'ups_info': '10 KVA Dedicated UPS Backup',
                'software_installed': 'Fedora / Ubuntu Linux, Lex & Yacc, OPNET Simulator, NASM Assembler, Java',
                'image_url': 'https://digitalveda.co.in/srm-valliammai/uploads/51ba570fe68fc088e0a942bdf8700cdce7eb8b1d/1775823176cse-lab-iii.webp',
                'display_order': 3
            },
            {
                'name': 'Larry Ellison Lab (Computer Programming & Systems Lab)',
                'domain': 'Enterprise Software Development, Core Programming & AI Models',
                'computers_count': 35,
                'printers_count': 4,
                'ups_info': '10 KVA Dedicated UPS Backup',
                'software_installed': 'Python 3.12, PyTorch, Java SDK, Apache Tomcat, Oracle Client, Visual Studio Code',
                'image_url': 'https://digitalveda.co.in/srm-valliammai/uploads/51ba570fe68fc088e0a942bdf8700cdce7eb8b1d/1775823182cse-lab-iv.webp',
                'display_order': 4
            },
            {
                'name': 'Charles Babbage Lab (Graphics & CASE Tools Lab)',
                'domain': 'Computer Graphics, Software Architecture & UML Modeling',
                'computers_count': 35,
                'printers_count': 3,
                'ups_info': '10 KVA Dedicated UPS Backup',
                'software_installed': 'OpenGL, Visual Studio, Rational Rose Enterprise, StarUML, Adobe Suite, Blender',
                'image_url': 'https://digitalveda.co.in/srm-valliammai/uploads/51ba570fe68fc088e0a942bdf8700cdce7eb8b1d/1775823201cse-lab-v.webp',
                'display_order': 5
            },
            {
                'name': 'Ken Thompson Lab (Open Source & Internet Programming Lab)',
                'domain': 'Full Stack Web Engineering, Microservices & Open Source Systems',
                'computers_count': 35,
                'printers_count': 2,
                'ups_info': '10 KVA + 5 KVA Dual UPS Backup',
                'software_installed': 'Node.js, Docker, NetBeans, Python Django/FastAPI, MongoDB, PostgreSQL, React tools',
                'image_url': 'https://digitalveda.co.in/srm-valliammai/uploads/51ba570fe68fc088e0a942bdf8700cdce7eb8b1d/1775823207cse-lab-vi.webp',
                'display_order': 6
            },
            {
                'name': 'Donald D. Chamberlin PG Research Lab',
                'domain': 'Postgraduate Research, Advanced AI/ML & Doctoral Projects',
                'computers_count': 19,
                'printers_count': 1,
                'ups_info': '10 KVA Dedicated UPS Backup',
                'software_installed': 'High Performance Linux, MATLAB, TensorFlow, PyTorch, Oracle 19c, NS-3 Simulator',
                'image_url': 'https://digitalveda.co.in/srm-valliammai/uploads/51ba570fe68fc088e0a942bdf8700cdce7eb8b1d/1775823212cse-lab-vii.webp',
                'display_order': 7
            },
        ]

        l_count = 0
        for lab in labs_data:
            _, created = DepartmentLab.objects.update_or_create(
                name=lab['name'],
                defaults=lab
            )
            if created:
                l_count += 1

        # 4. Department Official Milestones
        milestones_data = [
            {
                'title': 'Years of Excellence',
                'metric_value': '25+',
                'icon': 'fa-solid fa-trophy',
                'description': 'Established in 1999, accredited by NBA & NAAC with A Grade.',
                'display_order': 1
            },
            {
                'title': 'Placements in 2023',
                'metric_value': '149+',
                'icon': 'fa-solid fa-briefcase',
                'description': '800+ total campus placement offers secured across leading Tier-1 tech giants.',
                'display_order': 2
            },
            {
                'title': 'Advanced Computing Labs',
                'metric_value': '8',
                'icon': 'fa-solid fa-server',
                'description': '6 UG Laboratories + 1 PG Research Lab + 1 Central Server Cluster.',
                'display_order': 3
            },
            {
                'title': 'Research Journals & Papers',
                'metric_value': '100+',
                'icon': 'fa-solid fa-book-open',
                'description': 'Published in Scopus, IEEE, and Anna University recognized research centre.',
                'display_order': 4
            },
            {
                'title': 'Annual Intake (UG + PG)',
                'metric_value': '198',
                'icon': 'fa-solid fa-graduation-cap',
                'description': '180 B.E. Computer Science & Engineering + 18 M.E. CSE students.',
                'display_order': 5
            },
            {
                'title': 'Department Library Volumes',
                'metric_value': '724+',
                'icon': 'fa-solid fa-book-bookmark',
                'description': 'Specialized books and 112 foreign authored reference titles.',
                'display_order': 6
            },
        ]

        m_count = 0
        for m in milestones_data:
            _, created = DepartmentMilestone.objects.update_or_create(
                title=m['title'],
                defaults=m
            )
            if created:
                m_count += 1

        self.stdout.write(self.style.SUCCESS(
            f'Seeded: {p_count} placements, {d_count} documents, {l_count} labs, {m_count} milestones.'
        ))
