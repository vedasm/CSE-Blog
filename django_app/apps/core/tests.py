import pytest
from django.urls import reverse
from apps.accounts.models import AdminUser
from apps.core.models import DepartmentDocument, PlacementStat, DepartmentLab, DepartmentMilestone


@pytest.mark.django_db
def test_public_department_pages(client):
    # Setup sample data
    PlacementStat.objects.create(
        year=2023,
        students_placed=149,
        total_offers=165,
        highest_package='12 LPA',
        average_package='4.5 LPA',
        top_recruiters='TCS, CTS, Wipro, Infosys, Zoho'
    )
    DepartmentDocument.objects.create(
        title='Publications of Journals 2022–2023',
        category=DepartmentDocument.Category.RESEARCH,
        academic_year='2022-2023',
        description='Scopus listed publications',
        external_url='https://example.com/research.pdf'
    )
    DepartmentDocument.objects.create(
        title='Department Achievements 2021 to 2023',
        category=DepartmentDocument.Category.ACHIEVEMENT,
        academic_year='2021-2023',
        description='Hackathon wins',
        external_url='https://example.com/achievements.pdf'
    )
    DepartmentLab.objects.create(
        name='James Gosling Lab',
        domain='Networks & DBMS',
        computers_count=35
    )
    DepartmentMilestone.objects.create(
        title='Years of Excellence',
        metric_value='25+'
    )

    # 1. Home Page
    res = client.get(reverse('core:home'))
    assert res.status_code == 200
    assert b'25+' in res.content
    assert b'Department Records' in res.content

    # 2. Placements Page
    res = client.get(reverse('core:placements'))
    assert res.status_code == 200
    assert b'149' in res.content
    assert b'Placement Track Record' in res.content

    # 3. Research Page
    res = client.get(reverse('core:research'))
    assert res.status_code == 200
    assert b'Publications of Journals 2022' in res.content

    # 4. Achievements Page
    res = client.get(reverse('core:achievements'))
    assert res.status_code == 200
    assert b'Department Achievements' in res.content

    # 5. Infrastructure Page
    res = client.get(reverse('core:infrastructure'))
    assert res.status_code == 200
    assert b'James Gosling Lab' in res.content


@pytest.mark.django_db
def test_admin_can_manage_documents(client):
    admin_user = AdminUser.objects.create_user(
        email='hod.cse@srmvalliammai.ac.in',
        password='StrongPassword123!',
        role='superadmin'
    )
    client.force_login(admin_user)

    # Test list documents
    res = client.get(reverse('core_admin:manage_documents'))
    assert res.status_code == 200

    # Test create document
    add_url = reverse('core_admin:add_document')
    post_data = {
        'title': 'Test Anna Univ Research Centre Order',
        'category': DepartmentDocument.Category.RESEARCH,
        'academic_year': '2023-2024',
        'description': 'Official recognition circular',
        'external_url': 'https://example.com/order.pdf',
        'display_order': 1,
        'is_published': True,
    }
    res = client.post(add_url, post_data)
    assert res.status_code == 302
    assert DepartmentDocument.objects.filter(title='Test Anna Univ Research Centre Order').exists()

    doc = DepartmentDocument.objects.get(title='Test Anna Univ Research Centre Order')

    # Test edit document
    edit_url = reverse('core_admin:edit_document', kwargs={'pk': doc.pk})
    res = client.post(edit_url, {
        'title': 'Updated Anna Univ Research Centre Order',
        'category': DepartmentDocument.Category.RESEARCH,
        'academic_year': '2023-2024',
        'description': 'Updated description',
        'external_url': 'https://example.com/order.pdf',
        'display_order': 1,
        'is_published': True,
    })
    assert res.status_code == 302
    doc.refresh_from_db()
    assert doc.title == 'Updated Anna Univ Research Centre Order'

    # Test delete document
    del_url = reverse('core_admin:delete_document', kwargs={'pk': doc.pk})
    res = client.post(del_url)
    assert res.status_code == 302
    assert not DepartmentDocument.objects.filter(pk=doc.pk).exists()


@pytest.mark.django_db
def test_admin_can_manage_placements_and_labs(client):
    admin_user = AdminUser.objects.create_user(
        email='editor.cse@srmvalliammai.ac.in',
        password='StrongPassword123!',
        role='editor'
    )
    client.force_login(admin_user)

    placement_data = {
        'year': 2026,
        'students_placed': 180,
        'total_offers': 195,
        'highest_package': '18 LPA',
        'average_package': '6 LPA',
        'top_recruiters': 'Zoho, TCS, Infosys',
        'display_order': 0,
        'is_published': True,
    }
    response = client.post(reverse('core_admin:add_placement'), placement_data)
    assert response.status_code == 302
    placement = PlacementStat.objects.get(year=2026)
    assert client.get(reverse('core_admin:manage_placements')).status_code == 200

    placement_data['students_placed'] = 181
    response = client.post(reverse('core_admin:edit_placement', kwargs={'pk': placement.pk}), placement_data)
    assert response.status_code == 302
    placement.refresh_from_db()
    assert placement.students_placed == 181

    lab_data = {
        'name': 'AI Innovation Lab',
        'domain': 'Artificial Intelligence',
        'computers_count': 40,
        'printers_count': 2,
        'ups_info': '20 KVA',
        'software_installed': 'Python, PyTorch',
        'image_url': '',
        'display_order': 1,
    }
    response = client.post(reverse('core_admin:add_lab'), lab_data)
    assert response.status_code == 302
    lab = DepartmentLab.objects.get(name='AI Innovation Lab')
    assert client.get(reverse('core_admin:manage_labs')).status_code == 200
    response = client.post(reverse('core_admin:delete_lab', kwargs={'pk': lab.pk}))
    assert response.status_code == 302
    assert not DepartmentLab.objects.filter(pk=lab.pk).exists()
