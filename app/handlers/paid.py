from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from app.states import LogPaidHours
from app.sheets import get_sheet
from app.keyboards import main_kb

router = Router()

@router.message(F.text == "Оплачено")
async def ask_paid(msg: Message, state: FSMContext):
    await msg.answer("Введите количество оплаченных часов (пример: 4):")
    await state.set_state(LogPaidHours.WAIT_PAID_HOURS)

@router.message(LogPaidHours.WAIT_PAID_HOURS, F.text.regexp(r"^\d+(\.\d{1,2})?$"))
async def save_paid(msg: Message, state: FSMContext):
    ws = await get_sheet()
    await ws.append_row([msg.text])
    await msg.answer("✅ Записано!", reply_markup=main_kb)
    await state.clear()

@router.message(LogPaidHours.WAIT_PAID_HOURS)
async def invalid_paid(msg: Message):
    await msg.answer("Пожалуйста, введите число, можно с двумя цифрами после запятой.")
