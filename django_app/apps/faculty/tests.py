import pytest
from django.urls import reverse
from apps.accounts.models import AdminUser
from apps.faculty.models import Faculty


@pytest.mark.django_db
def test_public_faculty_profile_links(client):
    faculty = Faculty.objects.create(
        name='Dr. B. Vanathi',
        designation=Faculty.Designation.PROFESSOR,
        specialization='Artificial Intelligence, Computer Vision',
        email='hod.cse@srmvalliammai.ac.in',
        phone='+91 9841017713',
        profile_link='https://srmvalliammai.irins.org/profile/177877',
        bio='Professor & Head of Department'
    )

    # 1. Public faculty page
    res = client.get(reverse('public_faculty:list'))
    assert res.status_code == 200
    assert b'Dr. B. Vanathi' in res.content
    assert b'https://srmvalliammai.irins.org/profile/177877' in res.content
    assert b'View IRINS Profile' in res.content

    # 2. Homepage spotlight
    res_home = client.get(reverse('core:home'))
    assert res_home.status_code == 200
    assert b'https://srmvalliammai.irins.org/profile/177877' in res_home.content


@pytest.mark.django_db
def test_admin_can_manage_faculty_profile_link(client):
    admin_user = AdminUser.objects.create_user(
        email='admin@srmvalliammai.ac.in',
        password='StrongPassword123!',
        role='superadmin'
    )
    client.force_login(admin_user)

    faculty = Faculty.objects.create(
        name='Dr. M. Senthil Kumar',
        designation=Faculty.Designation.ASSOCIATE,
        specialization='Wireless Sensor Networks',
        email='senthilm@srmvalliammai.ac.in',
        phone='+91 9444123456',
        bio='Associate Professor',
        profile_link='https://srmvalliammai.irins.org/profile/177878'
    )

    edit_url = reverse('faculty:edit', kwargs={'pk': faculty.pk})
    res = client.get(edit_url)
    assert res.status_code == 200
    assert b'IRINS Faculty Profile URL' in res.content

    # Update profile link
    updated_url = 'https://srmvalliammai.irins.org/profile/177878-updated'
    res = client.post(edit_url, {
        'name': faculty.name,
        'designation': faculty.designation,
        'specialization': faculty.specialization,
        'email': faculty.email,
        'phone': faculty.phone,
        'profile_link': updated_url,
        'bio': faculty.bio,
        'display_order': 1,
        'is_active': True,
    })
    assert res.status_code == 302
    faculty.refresh_from_db()
    assert faculty.profile_link == updated_url
