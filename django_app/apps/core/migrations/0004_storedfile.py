from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0003_use_packaged_2022_2023_journal'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoredFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, unique=True)),
                ('content', models.BinaryField()),
                ('content_type', models.CharField(blank=True, max_length=150)),
                ('size', models.PositiveBigIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
