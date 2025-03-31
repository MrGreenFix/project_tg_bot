from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

keybord_random = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Закончить", callback_data="end")],
    [InlineKeyboardButton(text="Ещё один факт", callback_data="random")]
])


keybord_random2 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Закончить", callback_data="end")],
    [InlineKeyboardButton(text="Ещё один факт", callback_data="random")]
])


keybord_talk = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Альберт Эйнштейн", callback_data="talk_einstein")],
        [InlineKeyboardButton(text="Илон Маск", callback_data="talk_musk")],
        [InlineKeyboardButton(text="Закончить", callback_data="end")]
    ])


keybord_talk2 = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Закончить", callback_data="end")]
        ])


keyboard_quiz = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Наука", callback_data="quiz_science")],
        [InlineKeyboardButton(text="История", callback_data="quiz_history")],
        [InlineKeyboardButton(text="Закончить ❌", callback_data="end")]
    ])



keyboard_next_end = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Новый вопрос", callback_data="next_quiz")],
            [InlineKeyboardButton(text="Закончить", callback_data="end")]
        ])