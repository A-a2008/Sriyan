# Generated by Django 5.1.7 on 2025-04-01 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_remove_audio_date_of_upload_audio_datetime_of_upload'),
    ]

    operations = [
        migrations.AddField(
            model_name='audio',
            name='mood',
            field=models.CharField(choices=[('happy', 'Happy'), ('sad', 'Sad')], default='happy', max_length=10),
        ),
    ]
