from aiogram.fsm.state import StatesGroup, State

class LogWorkedHours(StatesGroup):
    WAIT_WORKED_HOURS = State()

class LogPaidHours(StatesGroup):
    WAIT_PAID_HOURS = State()

class CashIncome(StatesGroup):
    WAIT_CASH_IN_AMOUNT = State()
    WAIT_CASH_IN_COMMENT = State()

class CashExpense(StatesGroup):
    WAIT_CASH_OUT_AMOUNT = State()
    WAIT_CASH_OUT_COMMENT = State()

class CardExpense(StatesGroup):
    WAIT_CARD_OUT_AMOUNT = State()
    WAIT_CARD_OUT_COMMENT = State()

class Registration(StatesGroup):
    WAIT_LOCATION = State()
