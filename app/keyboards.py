from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("Отработано"), KeyboardButton("Оплачено")],
        [KeyboardButton("К оплате")],
        [KeyboardButton("Подотчет")],
        [KeyboardButton("Регистрация")],
    ],
    resize_keyboard=True,
)

cash_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("Наличные"), KeyboardButton("Карта")],
        [KeyboardButton("⬅️ Назад")],
    ],
    resize_keyboard=True,
)

cash_cash_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("Приход"), KeyboardButton("Расход")],
        [KeyboardButton("⬅️ Назад")],
    ],
    resize_keyboard=True,
)
