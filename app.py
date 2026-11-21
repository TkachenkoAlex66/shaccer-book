from flask import Flask, render_template, send_from_directory
import os
import re
import traceback

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_book():
    """Загружает текст книги и аккуратно разбивает на основные части"""
    book_path = os.path.join(BASE_DIR, "RUKOVODSTVO_SHACCER.txt")
    
    if not os.path.exists(book_path):
        return [{
            "title": "Ошибка",
            "content": f"Файл книги не найден: {book_path}"
        }]
    
    with open(book_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Более надёжное разбиение по основным частям
    parts = [
        ("Обложка и описание", r"(?s)^.*?ЧАСТЬ 1\."),
        ("Часть 1. Введение", r"(?s)ЧАСТЬ 1\..*?ЧАСТЬ 2\."),
        ("Часть 2. Знакомство с интерфейсом", r"(?s)ЧАСТЬ 2\..*?ЧАСТЬ 3\."),
        ("Часть 3. Строительство", r"(?s)ЧАСТЬ 3\..*?ЧАСТЬ 4\."),
        ("Часть 4. Текстуры", r"(?s)ЧАСТЬ 4\..*?ЧАСТЬ 5\."),
        ("Часть 5. Тестирование игры", r"(?s)ЧАСТЬ 5\..*?ЧАСТЬ 6\."),
        ("Часть 6. Полезные советы", r"(?s)ЧАСТЬ 6\..*?ЧАСТЬ 7\."),
        ("Часть 7. Заключение", r"(?s)ЧАСТЬ 7\..*"),
    ]

    chapters = []
    for title, pattern in parts:
        match = re.search(pattern, content)
        if match:
            text = match.group(0).strip()
            # Убираем следующий заголовок части, если он попал в конец
            if title != "Часть 7. Заключение":
                text = re.sub(r'\n═{5,}.*$', '', text, flags=re.DOTALL).strip()
                text = re.sub(r'ЧАСТЬ \d+\.\s*.*$', '', text, flags=re.DOTALL).strip()
            if text:
                chapters.append({"title": title, "content": text})

    # Если разбиение не сработало — отдаём всё целиком
    if len(chapters) < 3:
        chapters = [{
            "title": "Полное руководство SHACCER",
            "content": content
        }]

    return chapters


@app.route("/")
def index():
    try:
        chapters = load_book()
        return render_template("index.html", chapters=chapters)
    except Exception as e:
        return f"<h1>Ошибка на главной</h1><pre>{traceback.format_exc()}</pre>", 500


@app.route("/chapter/<int:num>")
def chapter(num):
    try:
        chapters = load_book()
        if 0 <= num < len(chapters):
            return render_template("chapter.html",
                                 chapter=chapters[num],
                                 num=num,
                                 total=len(chapters),
                                 chapters=chapters)
        return "Глава не найдена", 404
    except Exception as e:
        return f"<h1>Ошибка в главе</h1><pre>{traceback.format_exc()}</pre>", 500


@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory(os.path.join(BASE_DIR, "static"), filename)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
