from typing import List
from datetime import datetime
import logging

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.sheets import get_sheet
from app.keyboards import cash_kb, cash_cash_kb, main_kb
from app.states import CashIncome, CashExpense, CardExpense

router = Router()
logger = logging.getLogger(__name__)

# Столбцы Google Sheets
COLUMNS = {
    'DATE':     0,  # A
    'USER_ID':  1,  # B
    'TIME':     2,  # C
    'EMPTY_D':  3,  # D
    'EMPTY_E':  4,  # E
    'AMOUNT':   5,  # F
    'COMMENT':  6   # G
}

COLUMNS_COUNT = 7  # Фиксированное количество столбцов

async def save_to_sheet(row: List[str], msg: Message, state: FSMContext):
    """
    Записывает row в Google Sheets, отвечает пользователю и логирует результат.
    Всегда очищает состояние FSMContext.
    """
    try:
        logger.debug(f"Saving row to sheet: {row}")
        logger.debug(f"Row length: {len(row)}")
        
        ws = await get_sheet()
        await ws.append_row(row)
        await msg.answer("✅ Записано!", reply_markup=main_kb)
        logger.info(f"Successfully saved to sheet: {row}")
    except Exception as e:
        await msg.answer("❌ Ошибка при записи. Попробуйте позже.")
        logger.error(f"Error saving to sheet: {e}")
    finally:
        await state.clear()

# 1) Главное меню «Подотчет»
@router.message(F.text == "Подотчет")
async def show_cash_menu(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer("Выберите:", reply_markup=cash_kb)

# 2) Подменю наличных/карты
@router.message(F.text == "Наличные")
async def show_cash_cash_menu(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer("Выберите:", reply_markup=cash_cash_kb)

@router.message(F.text == "Карта")
async def start_card_expense(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer("Введите сумму расхода по карте (пример: 300.00):")
    await state.set_state(CardExpense.WAIT_CARD_OUT_AMOUNT)

# 3) Приход наличных
@router.message(F.text == "Приход")
async def start_cash_income(msg: Message, state: FSMContext):
    await msg.answer("Введите сумму прихода (пример: 1200.00):")
    await state.set_state(CashIncome.WAIT_CASH_IN_AMOUNT)

@router.message(CashIncome.WAIT_CASH_IN_AMOUNT, F.text.regexp(r"^\d+(\.\d{1,2})?$"))
async def cash_income_amount(msg: Message, state: FSMContext):
    await state.update_data(amount=msg.text)
    await msg.answer("Введите комментарий:")
    await state.set_state(CashIncome.WAIT_CASH_IN_COMMENT)

@router.message(CashIncome.WAIT_CASH_IN_AMOUNT)
async def cash_income_invalid(msg: Message):
    await msg.answer("❌ Неверный формат. Введите число (пример: 1200.00).")

@router.message(CashIncome.WAIT_CASH_IN_COMMENT)
async def cash_income_comment(msg: Message, state: FSMContext):
    data = await state.get_data()
    amount = data["amount"]
    now = datetime.now()

    # Создаем массив правильного размера
    row: List[str] = [""] * COLUMNS_COUNT
    row[COLUMNS['DATE']]    = now.strftime("%Y-%m-%d")
    row[COLUMNS['USER_ID']] = str(msg.from_user.id)
    row[COLUMNS['TIME']]    = now.strftime("%H:%M:%S")
    row[COLUMNS['AMOUNT']]  = amount
    row[COLUMNS['COMMENT']] = f"Приход наличных: {msg.text}"

    logger.debug(f"Cash income row: {row}")
    await save_to_sheet(row, msg, state)

# 4) Расход наличных
@router.message(F.text == "Расход")
async def start_cash_expense(msg: Message, state: FSMContext):
    await msg.answer("Введите сумму расхода (пример: 450.50):")
    await state.set_state(CashExpense.WAIT_CASH_OUT_AMOUNT)

@router.message(CashExpense.WAIT_CASH_OUT_AMOUNT, F.text.regexp(r"^\d+(\.\d{1,2})?$"))
async def cash_expense_amount(msg: Message, state: FSMContext):
    await state.update_data(amount=msg.text)
    await msg.answer("Введите комментарий:")
    await state.set_state(CashExpense.WAIT_CASH_OUT_COMMENT)

@router.message(CashExpense.WAIT_CASH_OUT_AMOUNT)
async def cash_expense_invalid(msg: Message):
    await msg.answer("❌ Неверный формат. Введите число (пример: 450.50).")

@router.message(CashExpense.WAIT_CASH_OUT_COMMENT)
async def cash_expense_comment(msg: Message, state: FSMContext):
    data = await state.get_data()
    amount = data["amount"]
    now = datetime.now()

    row: List[str] = [""] * COLUMNS_COUNT
    row[COLUMNS['DATE']]    = now.strftime("%Y-%m-%d")
    row[COLUMNS['USER_ID']] = str(msg.from_user.id)
    row[COLUMNS['TIME']]    = now.strftime("%H:%M:%S")
    row[COLUMNS['AMOUNT']]  = amount
    row[COLUMNS['COMMENT']] = f"Расход наличных: {msg.text}"

    logger.debug(f"Cash expense row: {row}")
    await save_to_sheet(row, msg, state)

# 5) Расход по карте
@router.message(CardExpense.WAIT_CARD_OUT_AMOUNT, F.text.regexp(r"^\d+(\.\d{1,2})?$"))
async def card_expense_amount(msg: Message, state: FSMContext):
    await state.update_data(amount=msg.text)
    await msg.answer("Введите комментарий:")
    await state.set_state(CardExpense.WAIT_CARD_OUT_COMMENT)

@router.message(CardExpense.WAIT_CARD_OUT_AMOUNT)
async def card_expense_invalid(msg: Message):
    await msg.answer("❌ Неверный формат. Введите число (пример: 300.00).")

@router.message(CardExpense.WAIT_CARD_OUT_COMMENT)
async def card_expense_comment(msg: Message, state: FSMContext):
    data = await state.get_data()
    amount = data["amount"]
    now = datetime.now()

    row: List[str] = [""] * COLUMNS_COUNT
    row[COLUMNS['DATE']]    = now.strftime("%Y-%m-%d")
    row[COLUMNS['USER_ID']] = str(msg.from_user.id)
    row[COLUMNS['TIME']]    = now.strftime("%H:%M:%S")
    row[COLUMNS['AMOUNT']]  = amount
    row[COLUMNS['COMMENT']] = f"Расход по карте: {msg.text}"

    logger.debug(f"Card expense row: {row}")
    await save_to_sheet(row, msg, state)

# 6) Обработчик «⬅️ Назад» - ДОЛЖЕН БЫТЬ ПОСЛЕДНИМ!
@router.message(F.text == "⬅️ Назад")
async def go_back(msg: Message, state: FSMContext):
    current = await state.get_state()
    logger.debug(f"Back button pressed by user {msg.from_user.id}. Current state: {current}")
    
    await state.clear()

    if current:
        if current.startswith("CashIncome") or current.startswith("CashExpense"):
            await msg.answer("Выберите:", reply_markup=cash_cash_kb)
        elif current.startswith("CardExpense"):
            await msg.answer("Выберите:", reply_markup=cash_kb)
        else:
            await msg.answer("Привет! Выберите действие:", reply_markup=main_kb)
    else:
        await msg.answer("Привет! Выберите действие:", reply_markup=main_kb)
