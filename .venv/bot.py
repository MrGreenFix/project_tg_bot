import asyncio
import logging

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

import config
import gpt
import keyboard
import until
import weather
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import  Message, CallbackQuery
from aiogram.filters import Command

from quiz_game import quiz_command
from until import send_photo

# Настройки
TOKEN_TG = config.TOKEN_TG
logging.basicConfig(level=logging.INFO)

# Инициализация бота
bot = Bot(token=TOKEN_TG)
dp = Dispatcher()


async def main_menu_start():
    commands = [
        types.BotCommand(command="start", description="Главное меню бота"),
        types.BotCommand(command="random", description="Случайный факт"),
        types.BotCommand(command="gpt", description="Общение с искусственным интеллектом"),
        types.BotCommand(command="talk", description="Диалог с известной личностью"),
        types.BotCommand(command="quiz", description="Игра в Квиз"),
        types.BotCommand(command="weather", description="Прогноз погоды"),
    ]
    await bot.set_my_commands(commands)


# /start
@dp.message(Command("start"))
async def start(message: types.Message):
    await until.send_photo(message, "promo")
    promt_text = until.send_text("promt")
    await message.answer(promt_text)

# /weather
class WeatherState(StatesGroup):
    waiting_for_city = State()

# /weather
@dp.message(Command("weather"))
async def weather_command(message: Message, state: FSMContext):
    await until.send_photo(message, "weather")
    await message.answer("Введи название города:")  # Сообщение в чат
    await state.set_state(WeatherState.waiting_for_city)


@dp.message(WeatherState.waiting_for_city)
async def city_handler(message: Message, state: FSMContext):
    city = message.text.strip()
    weather_info = weather.get_weather(city, config.TOKEN_WEATHER)
    await message.reply(weather_info)
    await state.clear()


# /random
@dp.message(Command("random"))
async def random(message: types.Message):
    await until.send_photo(message, "random")
    fact_random = await gpt.gpt_service.send_message("Расскажи научный факт")
    await message.answer(f"{fact_random}", reply_markup=keyboard.keybord_random)


# Обработчик кнопки (ещё факт)
@dp.callback_query(F.data == "random")
async def random_fact_callback(callback: types.CallbackQuery):
    fact_random = await gpt.gpt_service.send_message("Расскажи ещё один другой случайный научный факт.")
    await callback.message.answer(f"{fact_random}", reply_markup=keyboard.keybord_random2)
    await callback.answer()


# /gpt
@dp.message(Command("gpt"))
async def gpt_command(message: types.Message):
    await until.send_photo(message, "Clippy")
    await message.answer("Напиши свой вопрос ChatGPT.")


# / Ответ GPT
@dp.message(F.text)
async def handle_gpt_message(message: types.Message):
    answer_gpt = await gpt.gpt_service.send_message(user_message=message.text)
    await message.answer(answer_gpt)


# /talk
@dp.message(Command("talk"))
async def talk_comand(message: types.Message):
    await until.send_photo(message, "Dialogue")
    await message.answer("Выберите с кем хотите начать разговор", reply_markup=keyboard.keybord_talk)


user_talk_mode = {}
talk_prompts = {
    "talk_einstein": "Ты Альберт Эйнштейн. Отвечай как он.",
    "talk_musk": "Ты Илон Маск. Отвечай как он."
}


# выбор персонажа
@dp.callback_query(lambda c: c.data.startswith("talk_"))
async def talk_selection(callback: CallbackQuery):
    user_id = callback.from_user.id
    character = callback.data  #  talk_einstein

    user_talk_mode[user_id] = talk_prompts.get(character, "Отвечай дружелюбно и интересно.")

    await callback.message.answer(
        f"Теперь ты говоришь с {character.replace('talk_', '').title()}! Напиши ему сообщение.")
    await callback.answer()


# сообщения во время разговора
@dp.message()
async def handle_talk_message(message: Message):
    user_id = message.from_user.id


    if user_id not in user_talk_mode:
        await message.answer("Сначала выберите собеседника с помощью команды /talk.")
        return


    prompt = user_talk_mode[user_id]
    response = await gpt.gpt_service.send_message(f"{prompt}\n\nПользователь: {message.text}")

    await message.answer(response)


@dp.message(Command("quiz"))
async def quiz_handler(message: types.Message):
    await until.send_photo(message, "kviz")
    await quiz_command(message)


# Обработчик кнопки "Закончить"
@dp.callback_query(F.data == "end")
async def end_callback(callback: types.CallbackQuery):
    await start(callback.message)
    await callback.answer()


# === Запуск ===
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
