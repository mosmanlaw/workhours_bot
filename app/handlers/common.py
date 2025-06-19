from aiogram import Router, F
from aiogram.types import Message
import logging

from app.sheets import get_sheet
from app.keyboards import main_kb

router = Router()
logger = logging.getLogger(__name__)

@router.message(F.text.in_(["К оплате", "/start"]))
async def to_pay(msg: Message):
    try:
        ws = await get_sheet()
        vals = await ws.get_all_values()
        
        if len(vals) < 2:
            await msg.answer("Нет данных для расчета.", reply_markup=main_kb)
            return
            
        # Предполагаем, что столбец с отработанными часами - F (индекс 5)
        col_worked = 6  # F столбец (1-based)
        
        # Безопасное вычисление суммы с обработкой ошибок
        worked = 0
        for r in vals[1:]:  # Пропускаем заголовок
            if len(r) >= col_worked and r[col_worked-1]:
                try:
                    # Проверяем, что значение можно конвертировать в float
                    value = r[col_worked-1].strip()
                    if value and value.replace('.', '').replace('-', '').isdigit():
                        worked += float(value)
                except (ValueError, IndexError) as e:
                    logger.warning(f"Skipping invalid value: {r[col_worked-1]} - {e}")
                    continue
        
        await msg.answer(f"К оплате: {worked} ₽", reply_markup=main_kb)
        
    except Exception as e:
        logger.error(f"Error in to_pay: {e}")
        await msg.answer("❌ Ошибка при получении данных. Попробуйте позже.", reply_markup=main_kb)

@router.message()
async def echo(msg: Message):
    await msg.answer("Привет! Выберите действие:", reply_markup=main_kb)
