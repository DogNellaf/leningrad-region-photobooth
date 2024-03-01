import os

from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage
django.set

STATIC_DIR = "G:\\SBOS Work\\1. Programming\\2024\\02-4 - leningrad-region-photobooth\\photobooth\\static"

email = 'me@dognellaf.ru'
photo_name = 'images\\2024-03-01180638.png'
photo_url = os.path.join(STATIC_DIR, photo_name)

snap_name = 'snap-2024-03-01130139.png'
snap_url = os.path.join(STATIC_DIR, 'images')
snap_url = os.path.join(snap_url, snap_name) 

msg = EmailMultiAlternatives(
    "Фото с сайта путешествиеполенобласти.рф",
    "photo",
    'leningradsckayaoblast@yandex.ru',
    [email]
)
msg.mixed_subtype = 'related'
msg.attach_alternative("", "text/html")
with open(photo_url, 'rb') as f:
    img = MIMEImage(f.read())
    img.add_header('Content-ID', '<{name}>'.format(name=photo_name))
    img.add_header('Content-Disposition', 'inline', filename=photo_name)
msg.attach(img)