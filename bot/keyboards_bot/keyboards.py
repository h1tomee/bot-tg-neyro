from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_kb():
    kb = [
        [KeyboardButton(text="/chat"),
         KeyboardButton(text="/stop_chat"),
         KeyboardButton(text="/choose_gemini")]
    ]
    return ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите нейросеть"
    )