# Generated by Django 5.1.1 on 2024-10-22 23:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parsingModule', '0002_resume_resume_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resume',
            name='extracted_text',
        ),
    ]
