from random import randint
from aiogram import F, types, Router
from aiogram.filters import Command
from aiogram.utils.chat_action import ChatActionSender
from bot.constaints import GREETING, FILE_PROCESSING_ERROR, AUDIO_PROCESSING_ERROR
from bot.utils import translated_voice_to_text, handle_file
from main import bot

router = Router()


@router.message(Command("start"))
async def greeting(message: types.Message):
    await message.answer(GREETING)


@router.message(F.voice)
async def message_voice_handler(message: types.Message):
    async with ChatActionSender.typing(chat_id=message.chat.id, bot=bot):
        random_name_for_file = randint(0, 100000000)
        voice_id = message.voice.file_id
        try:
            voice = await bot.get_file(voice_id)
            full_path_to_file = await handle_file(file=voice, file_name=f"{random_name_for_file}.mp3", path="files/voices")
        except:
            await message.answer(FILE_PROCESSING_ERROR)
        else:
            try:
                text_from_voice = translated_voice_to_text(
                    file_path=full_path_to_file)
            except:
                await message.answer(AUDIO_PROCESSING_ERROR)
            else:
                await message.answer(text_from_voice)
