from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faculty', '0004_alter_faculty_profile_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faculty',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='faculty',
            name='phone',
            field=models.CharField(blank=True, max_length=15),
        ),
    ]