from django.db import migrations


def use_packaged_journal(apps, schema_editor):
    DepartmentDocument = apps.get_model('core', 'DepartmentDocument')
    DepartmentDocument.objects.filter(
        title='Publications of Journals 2022–2023',
    ).update(
        pdf_file=None,
        external_url='/static/documents/journal_22-23.pdf',
    )


def restore_external_journal(apps, schema_editor):
    DepartmentDocument = apps.get_model('core', 'DepartmentDocument')
    DepartmentDocument.objects.filter(
        title='Publications of Journals 2022–2023',
        external_url='/static/documents/journal_22-23.pdf',
    ).update(
        external_url='https://digitalveda.co.in/srm-valliammai/uploads/51ba570fe68fc088e0a942bdf8700cdce7eb8b1d/1775901940srm-vec-cse-list-of-journals-from-july-2022-june-2023.pdf',
    )


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0002_departmentdocument_departmentlab_departmentmilestone_and_more'),
    ]

    operations = [
        migrations.RunPython(use_packaged_journal, restore_external_journal),
    ]
