from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from app.states import LogWorkedHours
from app.sheets import get_sheet
from app.keyboards import main_kb

router = Router()

@router.message(F.text == "Отработано")
async def ask_worked(msg: Message, state: FSMContext):
    await msg.answer("Введите количество отработанных часов (пример: 8.5):")
    await state.set_state(LogWorkedHours.WAIT_WORKED_HOURS)

@router.message(LogWorkedHours.WAIT_WORKED_HOURS, F.text.regexp(r"^\d+(\.\d{1,2})?$"))
async def save_worked(msg: Message, state: FSMContext):
    ws = await get_sheet()
    await ws.append_row([msg.text])
    await msg.answer("✅ Записано!", reply_markup=main_kb)
    await state.clear()

@router.message(LogWorkedHours.WAIT_WORKED_HOURS)
async def invalid_worked(msg: Message):
    await msg.answer("Пожалуйста, введите число, можно с двумя цифрами после запятой.")
