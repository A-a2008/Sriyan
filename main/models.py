from django.db import models

# Create your models here.


class Audio(models.Model):
    MOOD_CHOICES = [
        ("happy", "Happy"),
        ("sad", "Sad"),
    ]
    
    audio_file = models.FileField(upload_to="audio_files/%Y/%m/%d/")
    datetime_of_upload = models.DateTimeField(auto_now=True)
    transcript = models.TextField()
    mood = models.CharField(max_length=10, choices=MOOD_CHOICES, default="happy")

    def __str__(self):
        return f"{self.mood} - {self.audio_file.name}"
