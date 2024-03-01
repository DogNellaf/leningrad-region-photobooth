from django.shortcuts import render, redirect
from django.http import JsonResponse
from datetime import datetime as dt, timedelta as td, timezone as tz
import photobooth.settings as settings
from photobooth.settings import STATICFILES_DIRS, EMAIL_HOST_USER
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMultiAlternatives, send_mail
from email.mime.image import MIMEImage
import os
import base64
from rembg import remove

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
    # me = 'Название компании <{}>'.format(settings.EMAIL_HOST_USER)
    subject = 'Ваше фото'

    # attachments = {
    #     'photo.jpg': os.join(settings.MEDIA_ROOT, 'test_attachment.pdf')
    # }

    # now = tz.now()
    # delta_sec = -70 

    # scheduled_time = now + td(seconds=delta_sec)

    # send_mail(
    #    subject,
    #     "Here is the message.",
    #     settings.EMAIL_HOST_USER,
    #     [email],
    #     fail_silently=False,
    # )

    # headers = {'To': f'Получатель письма от компании <{email}>'}
    # send_mail(email, me, subject=subject,
    #         message="Ваше фото", html_message="Ваше фото",
    #         scheduled_time=scheduled_time, headers=headers, attachments=attachments)

    
    photo_name = request.POST['photo_url']
    photo_url = os.path.join(STATIC_DIR, photo_name)

    snap_name = request.POST['snap_url']
    snap_url = os.path.join(STATIC_DIR, 'images')
    snap_url = os.path.join(snap_url, snap_name) 

    msg = EmailMultiAlternatives(
        "Фото с сайта путешествиеполенобласти.рф",
        "Ваше фото",
        EMAIL_HOST_USER,
        [email]
    )
    msg.mixed_subtype = 'related'
    msg.attach_alternative("", "text/html")
    with open(photo_url, 'rb') as f:
        img = MIMEImage(f.read())
        img.add_header('Content-ID', '<{name}>'.format(name=photo_name))
        img.add_header('Content-Disposition', 'inline', filename=photo_name)
    msg.attach(img)
    msg.send()
    return redirect(result, photo_url=photo_name.split('/')[-1].split('\\')[-1], snap_url=snap_name)

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