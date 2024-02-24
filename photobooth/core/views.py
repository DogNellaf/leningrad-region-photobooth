from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime as dt
from photobooth.settings import STATICFILES_DIRS
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
import os
import base64
from rembg import remove
from PIL import Image

STATIC_DIR = STATICFILES_DIRS[0]

def index(request):
    return render(request, "index.html")

def snap(request):
    return render(request, "snap.html")

def location(request, snap_url):
    return render(request, "location.html", {'snap_url': snap_url})

def editor(request, snap_url, location_title):
    location_title = os.path.join("location", location_title)
    snap_url = os.path.join("snaps", snap_url)
    return render(request, "editor.html", {'location_title': location_title, 'snap_url': snap_url})

def result(request, photo_url, snap_url):
    photo_url = os.path.join("images", photo_url)
    return render(request, "result.html", {'photo_url': photo_url, 'snap_url': snap_url})

@csrf_exempt
def send_email(request):
    email = request.POST['email']
    send_mail(
        "Subject here",
        "Here is the message.",
        "from@example.com",
        [email],
        fail_silently=False,
    )
    pass

@csrf_exempt
def save_snap(request):
    if request.method == 'POST':
        image_raw = request.body

        data = base64.b64decode(image_raw)

        image_name = "snap-" + dt.now().strftime('%Y-%m-%d%H%I%S') + '.png'

        path = os.path.join(STATIC_DIR, 'snaps')
        path = os.path.join(path, image_name)

        # with open(path, 'wb') as f: 
        #     f.write(data)

        # input = Image.open(path)
        output = remove(data)
        # os.remove(path)
        # output.save(path)
        with open(path, 'wb') as f: 
            f.write(output)

        return JsonResponse({'success': True, 'image_name': image_name})
    return JsonResponse({'success': False, 'image_name': None})

@csrf_exempt
def save_image(request):
    if request.method == 'POST':
        image_raw = request.body

        data = base64.b64decode(image_raw)

        image_name = dt.now().strftime('%Y-%m-%d%H%I%S') + '.png'

        path = os.path.join(STATIC_DIR, 'images')
        path = os.path.join(path, image_name)

        with open(path, "wb") as out:
            out.write(data)

        return JsonResponse({'success': True, 'image_name': image_name})
    return JsonResponse({'success': False, 'image_name': None})