from aiogram import Router, types, F
from aiogram.filters import Command,StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from google import genai
from app.core.config import settings
from bot.keyboards_bot.keyboards import get_main_kb
import logging


#Настройки
logger = logging.getLogger(__name__)
router = Router()
MODEL_NAME = settings.model_name
client = genai.Client(api_key=settings.api_key.get_secret_value())

#Режим состояния пользователя
class ChatStates(StatesGroup):
    is_chatting = State()

#Ретраи если выходит ошибка
@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=2, min=15, max=60),
retry=retry_if_exception_type(Exception)
)
async def get_gemini_response(text: str):
    response = await client.aio.models.generate_content(
        model=MODEL_NAME,
        contents=text
    )
    return response



#Хендлеры для обработки команд
@router.message(Command("start"))
async def start_dialog(message: types.Message):
    await message.answer(
        f"Привет, {message.from_user.first_name}!\n"
        "Выбирай нейросеть",
        reply_markup=get_main_kb()
    )   
   
        
    
#Включение нейросети Gemini
@router.message(Command("choose_gemini"))
async def start_ai_gemini(message: types.Message, state: FSMContext):
    await state.set_state(
        ChatStates.is_chatting
    )
    await message.answer(
        "Режим нейросети включен, чтобы выйти введите /stop_chat"
        )
    

@router.message(Command("stop"))    
@router.message(Command("stop_chat"))
async def stop_ai_gemini(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Режим нейросети выключен")


@router.message(ChatStates.is_chatting)
async def active_ai_gemini(message: types.Message):
    #Если сообщение не является текстом
    if not message.text:
        return
    
    #Бот "печатает"
    await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")
    
    try:
        response = await get_gemini_response(message.text)
        await message.answer(response.text)
    
    
    except Exception as e:
        logger.error(f"Ошибка у пользователя {message.from_user.id}: {e}", exc_info=True)
        await message.answer("Произошла ошибка при обработке запроса.")
        
        
@router.message(F.text, ~StateFilter(ChatStates.is_chatting))
async def echo_off_mode(message: types.Message):
    await message.answer(
        "Вижу твое сообщение, но не могу на него ответить \n"
        "Чтобы пообщаться с ИИ напиши /choose_gemini"
    )