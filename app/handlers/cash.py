from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from app.states import CashIncome, CashExpense, CardExpense
from app.keyboards import cash_kb, cash_cash_kb, main_kb
from app.sheets import get_sheet

router = Router()

@router.message(F.text == "Подотчет")
async def cash_menu(msg: Message):
    await msg.answer("Выберите:", reply_markup=cash_kb)

@router.message(F.text == "Наличные")
async def cash_cash_menu(msg: Message):
    await msg.answer("Выберите:", reply_markup=cash_cash_kb)

@router.message(F.text == "Карта")
async def cash_card_start(msg: Message, state: FSMContext):
    await msg.answer("Введите сумму расхода по карте (пример: 300.00):")
    await state.set_state(CardExpense.WAIT_CARD_OUT_AMOUNT)

@router.message(CardExpense.WAIT_CARD_OUT_AMOUNT, F.text.regexp(r"^\d+(\.\d{1,2})?$"))
async def save_card(msg: Message, state: FSMContext):
    ws = await get_sheet()
    await ws.append_row([msg.text])
    await msg.answer("Введите комментарий:")
    await state.set_state(CardExpense.WAIT_CARD_OUT_COMMENT)

@router.message(CardExpense.WAIT_CARD_OUT_COMMENT)
async def save_card_comment(msg: Message, state: FSMContext):
    ws = await get_sheet()
    await ws.append_row([msg.text])
    await msg.answer("✅ Записано!", reply_markup=main_kb)
    await state.clear()

@router.message(F.text == "Приход")
async def cash_in_start(msg: Message, state: FSMContext):
    await msg.answer("Введите сумму прихода (пример: 1200.00):")
    await state.set_state(CashIncome.WAIT_CASH_IN_AMOUNT)

@router.message(CashIncome.WAIT_CASH_IN_AMOUNT, F.text.regexp(r"^\d+(\.\d{1,2})?$"))
async def save_cash_in(msg: Message, state: FSMContext):
    ws = await get_sheet()
    await ws.append_row([msg.text])
    await msg.answer("Введите комментарий:")
    await state.set_state(CashIncome.WAIT_CASH_IN_COMMENT)

@router.message(CashIncome.WAIT_CASH_IN_COMMENT)
async def save_cash_in_comment(msg: Message, state: FSMContext):
    ws = await get_sheet()
    await ws.append_row([msg.text])
    await msg.answer("✅ Записано!", reply_markup=main_kb)
    await state.clear()

@router.message(F.text == "Расход")
async def cash_out_start(msg: Message, state: FSMContext):
    await msg.answer("Введите сумму расхода (пример: 450.50):")
    await state.set_state(CashExpense.WAIT_CASH_OUT_AMOUNT)

@router.message(CashExpense.WAIT_CASH_OUT_AMOUNT, F.text.regexp(r"^\d+(\.\d{1,2})?$"))
async def save_cash_out(msg: Message, state: FSMContext):
    ws = await get_sheet()
    await ws.append_row([msg.text])
    await msg.answer("Введите комментарий:")
    await state.set_state(CashExpense.WAIT_CASH_OUT_COMMENT)

@router.message(CashExpense.WAIT_CASH_OUT_COMMENT)
async def save_cash_out_comment(msg: Message, state: FSMContext):
    ws = await get_sheet()
    await ws.append_row([msg.text])
    await msg.answer("✅ Записано!", reply_markup=main_kb)
    await state.clear()
