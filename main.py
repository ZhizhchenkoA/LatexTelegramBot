import logging
from bot.client import LatexBot

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

if __name__ == "__main__":
    app = LatexBot()
    print("🚀 Запуск LaTeX Userbot'а...")
    app.run()