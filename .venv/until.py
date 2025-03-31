import os

from aiogram import types
from aiogram.types import FSInputFile


# Загрузка текстовых сообщений
def send_text(name: str) -> str:
    path = f"message/{name}.txt"
    return open(path, "r", encoding="utf8").read() if os.path.exists(path) else "Файл не найден"



# Отправка фото
async def send_photo(message: types.Message, name: str):
    photo_path = f'pictures/{name}.jpg'

    # Проверяем, существует ли файл
    if not os.path.exists(photo_path):
        await message.answer("Ошибка: Файл изображения не найден!")
        return
    photo = FSInputFile(photo_path)
    await message.answer_photo(photo)