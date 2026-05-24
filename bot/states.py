from aiogram.fsm.state import StatesGroup, State

class Model(StatesGroup):
    ChoosingModel = State()
    WaitingForRequest = State()