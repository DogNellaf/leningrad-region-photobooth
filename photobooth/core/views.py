from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime as dt
from photobooth.settings import STATICFILES_DIRS
import os
from rembg import remove
from PIL import Image


def index(request):
    return render(request, "index.html")

def snap(request):
    return render(request, "snap.html")

def location(request):
    return render(request, "location.html")

def editor(request, location_title):
    location_title = 'location/' + location_title
    return render(request, "editor.html", {'location_title': location_title})

def result(request, photo_url):
    return render(request, "result.html", {'photo_url': os.path.join("images", photo_url)})

def save_snap(request):
    if request.method == 'POST':
        image_name = request.POST.get['image_name']
        if image_name:
            path = os.path.join(STATICFILES_DIRS[0], 'snaps')
            path = os.path.join(path, image_name)
            
            output = remove(Image.open(path))
            output.save(path)
            return JsonResponse({'success': True, 'image_name': image_name})
        return JsonResponse({'success': False, 'image_name': None})

def save_image(request):
    if request.method == 'POST':
        import re
        import base64

        image_raw = request.body

        data = base64.b64decode(image_raw)

        image_name = dt.now().strftime('%Y-%m-%d%H%I%S') + '.png'

        path = os.path.join(STATICFILES_DIRS[0], 'images')
        path = os.path.join(path, image_name)

        with open(path, "wb") as out:
            out.write(data)

        return JsonResponse({'success': True, 'image_name': image_name})
    return JsonResponse({'success': False, 'image_name': None})