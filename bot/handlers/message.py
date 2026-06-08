import logging
import config # Добавляем импорт конфига
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

    escape_word = config.config.ESCAPE_WORD
    if escape_word and text.startswith(escape_word):
        # Берем остаток строки после слова-исключения
        remainder = text[len(escape_word):]
        
        # Проверяем, что это именно отдельное слово (после него пробел, перенос строки или конец текста)
        # Это предотвращает срабатывание, если вы написали "rawr" или "rawdata"
        if not remainder or remainder[0] in (" ", "\n", "\t"):
            clean_text = remainder.strip()
            
            if clean_text:
                # Если после слова есть текст, просто отправляем/редактируем его как есть
                await message.edit(clean_text)
            else:
                # Если было только слово-исключение, удаляем сообщение, чтобы не отправлять пустоту
                await message.delete()
            
            # Прерываем функцию, LaTeX-конвертация НЕ выполняется
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
    await _process_and_convert_message(client, message)


@LatexBot.on_edited_message(filters.me)
async def auto_convert_edited_message(client: LatexBot, message: Message):
    await _process_and_convert_message(client, message)