from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils.timezone import make_aware
from django.conf import settings
import speech_recognition as sr
from django.apps import apps
import tempfile
import os
import datetime

recognizer = sr.Recognizer()

Audio = apps.get_model("main", "Audio")

# Create your views here.


def home(request):
    if request.method == "POST":
        audio_file = request.FILES["audio_file"]
        mood = request.POST.get("mood")
        transcript = ""

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            for chunk in audio_file.chunks():
                tmp_file.write(chunk)
            tmp_path = tmp_file.name

        try:
            with sr.AudioFile(tmp_path) as source:
                audio_data = recognizer.record(source)
                transcript = recognizer.recognize_google(audio_data)
        except sr.UnknownValueError:
            transcript = "Audio could not be understood"
        except sr.RequestError:
            transcript = "Could not request results from API"
        finally:
            os.unlink(tmp_path)

        Audio.objects.create(
            audio_file=audio_file,
            transcript=transcript,
            mood=mood
        )

        data = {
            "messages": ["Audio File added successfully"],
        }

        return render(request, "index.html", data)
    else:
        audio_files = Audio.objects.all()
        audio_files = Audio.objects.all()
        for audio in audio_files:
            audio.file_name = os.path.basename(audio.audio_file.name)

        data = {
            "audio_files": audio_files,
        }

        return render(request, 'index.html', data)


def get_updated_audio_files(request):
    last_update_str = request.GET.get("last_update", "")

    try:
        last_update_dt = datetime.datetime.fromisoformat(last_update_str)
        last_update_dt = make_aware(last_update_dt)
    except ValueError:
        return JsonResponse({"error": "Invalid datetime format"}, status=400)

    new_audio_files = Audio.objects.filter(datetime_of_upload__gt=last_update_dt)

    happy_files = [
        {
            "file_name": audio.audio_file.name,
            "file_url": request.build_absolute_uri(audio.audio_file.url),
            "upload_time": audio.datetime_of_upload.isoformat(),
        }
        for audio in new_audio_files if audio.mood == "happy"
    ]

    sad_files = [
        {
            "file_name": audio.audio_file.name,
            "file_url": request.build_absolute_uri(audio.audio_file.url),
            "upload_time": audio.datetime_of_upload.isoformat(),
        }
        for audio in new_audio_files if audio.mood == "sad"
    ]

    return JsonResponse({
        "happy": happy_files,
        "sad": sad_files
    })

