# leningrad-region-photobooth

Веб-фотобудка на Django для интерактивного "путешествия по Ленинградской области".

Пользовательский сценарий:
1. Открыть стартовый экран.
2. Сделать фото с веб-камеры (с таймером).
3. Автоматически вырезать фон (через `rembg`).
4. Выбрать локацию.
5. Разместить вырезанный силуэт на фоне в редакторе.
6. Получить итоговое изображение, скачать по QR-коду или отправить на email.

## Стек

- Python 3.10+
- Django 4.x
- rembg
- python-dotenv
- SQLite (по умолчанию)
- Frontend: шаблоны Django + Fabric.js + webcam-easy + QRCode.js

## Структура проекта

```text
.
├── run.bat
├── requirements.txt
├── photobooth/
│   ├── manage.py
│   ├── .env.example
│   ├── core/
│   │   ├── views.py
│   │   └── templates/
│   └── photobooth/
│       ├── settings.py
│       └── urls.py
└── static/
	├── images/   # итоговые изображения
	├── snaps/    # снимки с удаленным фоном
	├── location/ # фоновые локации
	└── ...
```

## Быстрый запуск (Windows)

В корне проекта:

```bat
run.bat
```

Скрипт автоматически:
- создаст виртуальное окружение `.venv` (если его нет),
- установит зависимости,
- запустит Django-сервер.

После запуска откройте:

```text
http://127.0.0.1:8000/
```

## Ручной запуск

1. Создайте и активируйте виртуальное окружение.

Windows (PowerShell):

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Установите зависимости:

```bash
pip install -r requirements.txt
```

3. Создайте файл переменных окружения:

```powershell
Copy-Item photobooth\.env.example photobooth\.env
```

4. Заполните `photobooth/.env` своими значениями (минимум `DJANGO_SECRET_KEY` и SMTP-параметры).

5. Перейдите в папку с `manage.py` и запустите сервер:

```bash
cd photobooth
python manage.py runserver
```

6. Откройте приложение:

```text
http://127.0.0.1:8000/
```

## Переменные окружения (.env)

Файл: `photobooth/.env`.

Обязательные переменные:
- `DJANGO_SECRET_KEY` - секретный ключ Django.
- `DJANGO_DEBUG` - `True`/`False`.
- `DJANGO_ALLOWED_HOSTS` - список хостов через запятую.
- `EMAIL_HOST` - SMTP-сервер.
- `EMAIL_PORT` - SMTP-порт.
- `EMAIL_USE_TLS` - `True`/`False`.
- `EMAIL_HOST_USER` - SMTP-логин.
- `EMAIL_HOST_PASSWORD` - SMTP-пароль или app-password.

Шаблон доступен в `photobooth/.env.example`.

## Маршруты

- `GET /` - стартовая страница.
- `GET /snap` - съемка фото с камеры.
- `GET /location/<snap_url>` - выбор локации.
- `GET /editor/<snap_url>/<location_title>` - редактор композиции.
- `GET /result/<snap_url>/<photo_url>` - экран результата.
- `POST /save_snap` - сохранить снимок после удаления фона.
- `POST /save_image` - сохранить итоговое изображение.
- `POST /send_email` - отправить фото на email.

## Email-отправка

Проект использует SMTP (настроено в `photobooth/settings.py`).

SMTP-параметры берутся из переменных окружения в `photobooth/.env`.

## Важные заметки

- Для работы съемки браузеру нужен доступ к веб-камере.
- Для `rembg` могут потребоваться дополнительные системные зависимости (в зависимости от ОС и окружения).
- Папки `static/images` и `static/snaps` должны существовать и быть доступны на запись.

## Проверка

В проекте есть заготовка `test.py`, но полноценный набор автоматических тестов не настроен.

## Лицензия

Apache License 2.0

## Статус проекта

Завершен