import logging
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import MessageNotModified

from bot.client import LatexBot
from utils.latex_converter import latex_to_unicode

logger = logging.getLogger(__name__)


async def _process_and_convert_message(client: LatexBot, message: Message):
    """
    Вспомогательная функция для конвертации LaTeX-команд в сообщении.
    """
    text = message.text or message.caption
    
    if not text:
        return

    if "\\" not in text and "^" not in text and "_" not in text:
        return

    try:
        # Конвертируем текст
        converted_text = latex_to_unicode(text)
        
        # Если текст изменился после конвертации, редактируем сообщение
        if converted_text != text:
            await message.edit(converted_text)
            
    except MessageNotModified:
        pass
    except Exception as e:
        logger.error(f"Ошибка при авто-конвертации сообщения: {e}")


@LatexBot.on_message(filters.me)
async def auto_convert_new_message(client: LatexBot, message: Message):
    """
    Автоматически конвертирует LaTeX-команды в новых исходящих сообщениях.
    """
    await _process_and_convert_message(client, message)


@LatexBot.on_edited_message(filters.me)
async def auto_convert_edited_message(client: LatexBot, message: Message):
    """
    Автоматически конвертирует LaTeX-команды при редактировании исходящих сообщений.
    """
    await _process_and_convert_message(client, message)