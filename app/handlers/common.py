from aiogram import Router, F
from aiogram.types import Message
from app.keyboards import main_kb
from app.sheets import get_sheet

router = Router()

@router.message(F.text == "/start")
async def start_handler(msg: Message):
    await msg.answer("Привет! Выберите действие:", reply_markup=main_kb)

@router.message(F.text == "/help")
async def help_handler(msg: Message):
    await msg.answer("/start – меню\n/help – справка")

@router.message(F.text == "К оплате")
async def to_pay(msg: Message):
    ws = await get_sheet()
    vals = await ws.get_all_values()
    col_worked, col_paid = 1, 2
    worked = sum(float(r[col_worked-1]) for r in vals[1:] if r[col_worked-1])
    paid   = sum(float(r[col_paid-1])   for r in vals[1:] if r[col_paid-1])
    await msg.answer(f"На сегодня к оплате {worked-paid:.2f} часов.")
