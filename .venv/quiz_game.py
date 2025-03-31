
from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import keyboard
from gpt import gpt_service

quiz_sessions = {}

quiz_prompts = {
    "quiz_science": "Задай мне вопрос по науке с 4 вариантами ответа. Укажи правильный ответ в конце, например: (Правильный ответ: A)",
    "quiz_history": "Задай исторический вопрос с 4 вариантами ответа. Укажи правильный ответ в конце, например: (Правильный ответ: B)"
}

async def quiz_command(message: types.Message):
    await message.answer("Выбери тему квиза:", reply_markup=keyboard.keyboard_quiz)

async def quiz_selection(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    topic = callback.data

    quiz_sessions[user_id] = {"topic": topic, "score": 0, "question_count": 0}
    await ask_quiz_question(callback.message, user_id)
    await callback.answer()

async def ask_quiz_question(message: types.Message, user_id):
    if quiz_sessions[user_id]["question_count"] >= 5:
        await end_quiz(message, user_id)
        return

    topic = quiz_sessions[user_id]["topic"]
    response = await gpt_service.send_message(quiz_prompts[topic])

    lines = response.split("\n")
    question = lines[0]
    options = lines[1:5]
    correct_answer = lines[-1].replace("Правильный ответ:", "").strip()

    quiz_sessions[user_id]["correct_answer"] = correct_answer
    quiz_sessions[user_id]["question_count"] += 1
    keyboard_ABCD = InlineKeyboardMarkup(inline_keyboard=[

        [InlineKeyboardButton(text=options[0], callback_data="answer_A")],
        [InlineKeyboardButton(text=options[1], callback_data="answer_B")],
        [InlineKeyboardButton(text=options[2], callback_data="answer_C")],
        [InlineKeyboardButton(text=options[3], callback_data="answer_D")]
    ])
    await message.answer(f"{question} (Вопрос {quiz_sessions[user_id]['question_count']}/5)", reply_markup=keyboard_ABCD)

async def handle_quiz_answer(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_answer = callback.data.split("_")[1]
    correct_answer = quiz_sessions[user_id].get("correct_answer")

    if correct_answer and user_answer == correct_answer:
        quiz_sessions[user_id]["score"] += 1
        await callback.message.answer("Правильно!")
    else:
        await callback.message.answer(f"Неверно. Правильный ответ: {correct_answer}")

    if quiz_sessions[user_id]["question_count"] >= 5:
        await end_quiz(callback.message, user_id)
    else:
        await callback.message.answer(f"🏆 Твой счёт: {quiz_sessions[user_id]['score']}", reply_markup=keyboard.keyboard_next_end)

    await callback.answer()

async def next_quiz(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await ask_quiz_question(callback.message, user_id)
    await callback.answer()

async def end_quiz(message: types.Message, user_id):
    score = quiz_sessions[user_id]["score"]
    total_questions = 5

    if score >= 3:
        result = f"Ты победил! {score}/{total_questions} правильных ответов! 🏆"
    else:
        result = f"🤖 ChatGPT победил! Ты набрал {score}/{total_questions} правильных ответов. Попробуй ещё раз!"

    await message.answer(result)
    del quiz_sessions[user_id]  # Очистка данных пользователя после завершения игры

async def end_callback(callback: types.CallbackQuery):
    quiz_sessions.pop(callback.from_user.id, None)
    await callback.message.answer("🏁 Квиз завершён! Напиши /quiz, чтобы начать заново.")
    await callback.answer()

def register_quiz_handlers(dp: Dispatcher):
    dp.callback_query.register(quiz_selection, lambda c: c.data.startswith("quiz_"))
    dp.callback_query.register(handle_quiz_answer, lambda c: c.data.startswith("answer_"))
    dp.callback_query.register(next_quiz, lambda c: c.data == "next_quiz")
    dp.callback_query.register(end_callback, lambda c: c.data == "end")


def options():
    return None