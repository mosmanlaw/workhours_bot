from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Отработано"), KeyboardButton(text="Оплачено")],
        [KeyboardButton(text="К оплате")],
        [KeyboardButton(text="Подотчет")],
        [KeyboardButton(text="Регистрация")],
    ],
    resize_keyboard=True,
)

cash_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Наличные"), KeyboardButton(text="Карта")],
        [KeyboardButton(text="⬅️ Назад")],
    ],
    resize_keyboard=True,
)

cash_cash_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Приход"), KeyboardButton(text="Расход")],
        [KeyboardButton(text="⬅️ Назад")],
    ],
    resize_keyboard=True,
)

