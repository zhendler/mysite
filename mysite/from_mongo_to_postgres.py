import pymongo
import django
import os
from dateutil import parser
from django.core.exceptions import ValidationError

# Ініціалізація Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from blog.models import Author, Post, Tag  # Імпортуємо ваші моделі Django

# Підключення до MongoDB
mongo_client = pymongo.MongoClient("mongodb+srv://zhen:passwordauth@cluster01.mijkw.mongodb.net/quotes_database?retryWrites=true&w=majority&appName=Cluster01")
mongo_db = mongo_client["quotes_database"]

# Колекції в MongoDB
authors_collection = mongo_db["authors"]
quotes_collection = mongo_db["quotes"]

# Функція для переносу авторів
def migrate_authors():
    for author_data in authors_collection.find():
        # Конвертуємо дату народження у формат YYYY-MM-DD
        birthdate_str = author_data.get("birthdate")
        birthdate = None
        if birthdate_str:
            try:
                birthdate = parser.parse(birthdate_str).date()
            except (ValueError, TypeError, OverflowError, ValidationError):
                print(f"Неправильний формат дати для автора {author_data.get('name')}: {birthdate_str}")

        # Створюємо або отримуємо автора
        Author.objects.get_or_create(
            name=author_data.get("name"),
            defaults={
                "birthdate": birthdate,
                "location": author_data.get("location"),
            }
        )
    print("Міграція авторів завершена.")

# Функція для переносу цитат
def migrate_quotes():
    for quote_data in quotes_collection.find():
        # Отримуємо або створюємо автора в PostgreSQL
        author_name = quote_data.get("author")
        author = Author.objects.filter(name=author_name).first()

        # Ігноруємо цитати без автора
        if not author:
            continue

        # Отримуємо текст цитати
        content = quote_data.get("text", '')

        # Перевірка поля title
        title = quote_data.get("title")
        if not title:  # Якщо title відсутнє
            title = content[:10]  # Використовуємо перші 10 символів з content

        # Створюємо запис цитати
        post, created = Post.objects.get_or_create(
            content=content,
            author=author,
            defaults={
                'title': title,  # Додаємо title
            }
        )

        # Додаємо теги, якщо вони існують
        tags = quote_data.get("tags", [])
        for tag_name in tags:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            post.tags.add(tag)

        post.save()
    print("Міграція цитат завершена.")

# Виконуємо функції міграції
migrate_authors()
migrate_quotes()
