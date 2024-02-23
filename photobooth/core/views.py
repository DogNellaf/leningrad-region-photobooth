from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime as dt
from photobooth.settings import STATICFILES_DIRS
from django.views.decorators.csrf import csrf_exempt
import os
import base64

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
def save_snap(request):
    if request.method == 'POST':
        image_raw = request.body

        data = base64.b64decode(image_raw)

        image_name = "snap-" + dt.now().strftime('%Y-%m-%d%H%I%S') + '.png'

        path = os.path.join(STATIC_DIR, 'snaps')
        path = os.path.join(path, image_name)

        with open(path, 'wb') as f: 
            f.write(data)

        # # input_path = 'input.png'
        # # output_path = 'output.png'
        # # Загрузка изображения
        # image = cv2.imread(path)
        # # Преобразование изображения в оттенки серого
        # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # # Применение порогового преобразования для выделения объекта
        # _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)

        # # Нахождение контуров на пороговом изображении
        # contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # # Создание маски для объекта
        # mask = np.zeros_like(image)
        # cv2.drawContours(mask, contours, -1, (255, 255, 255), thickness=cv2.FILLED)

        # # Инвертирование маски
        # mask_inv = cv2.bitwise_not(mask)

        # # Применение маски к исходному изображению для удаления фона
        # result = cv2.bitwise_and(image, image, mask=mask_inv)

        # # Сохранение результата
        # cv2.imwrite(path, result)

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