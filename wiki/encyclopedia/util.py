# encyclopedia/util.py

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import re


def list_entries():
    _, filenames = default_storage.listdir("entries")
    return sorted(
        re.sub(r"\.md$", "", filename)
        for filename in filenames
        if filename.endswith(".md")
    )


def save_entry(title, content):
    """Завжди зберігаємо в UTF-8"""
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)

    # ContentFile автоматично обробляє bytes/str
    default_storage.save(filename, ContentFile(content.encode("utf-8")))


def get_entry(title):
    """Завжди читаємо як UTF-8"""
    filename = f"entries/{title}.md"
    try:
        with default_storage.open(filename) as f:
            return f.read().decode("utf-8")
    except FileNotFoundError:
        return None
    except UnicodeDecodeError as e:
        # Допоміжне повідомлення під час розробки
        raise UnicodeDecodeError(
            e.encoding, e.object, e.start, e.end,
            f"Файл {filename} не в UTF-8! Перетвори його на UTF-8."
        ) from e