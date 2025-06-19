from aiogram import Router, F
from aiogram.types import Message, Location
from aiogram.fsm.context import FSMContext
from app.states import Registration
from app.keyboards import main_kb
from app.sheets import get_sheet

router = Router()

@router.message(F.text == "Регистрация")
async def ask_location(msg: Message, state: FSMContext):
    await msg.answer("Отправьте вашу локацию (кнопка «Поделиться»):")
    await state.set_state(Registration.WAIT_LOCATION)

@router.message(Registration.WAIT_LOCATION, F.location)
async def save_location(msg: Message, state: FSMContext):
    loc: Location = msg.location
    ws = await get_sheet()
    await ws.append_row([loc.latitude, loc.longitude])
    await msg.answer("✅ Локация сохранена!", reply_markup=main_kb)
    await state.clear()

@router.message(Registration.WAIT_LOCATION)
async def invalid_location(msg: Message):
    await msg.answer("Пожалуйста, отправьте геолокацию через кнопку «Поделиться».")
