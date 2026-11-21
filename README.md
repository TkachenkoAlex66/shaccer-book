# Электронная книга «Руководство инструмента SHACCER»

Красивая веб-версия руководства по 3D-платформе SHACCER.

## Как запустить локально

```bash
pip install -r requirements.txt
python app.py
```

Откройте http://127.0.0.1:5000

## Как выложить на Render.com

1. Создайте новый **Web Service** на [render.com](https://render.com)
2. Подключите этот репозиторий (или загрузите как ZIP)
3. Настройки:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
4. Нажмите Create Web Service

Готово! Сайт будет доступен по адресу вида `https://ваш-сервис.onrender.com`

## Структура

- `app.py` — основное приложение Flask
- `templates/` — HTML-шаблоны
- `static/cover.png` — обложка книги
- `RUKOVODSTVO_SHACCER.txt` — полный текст руководства
