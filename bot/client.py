from pyrogram import Client
import config

class LatexBot(Client):
    def __init__(self):
        client_kwargs = {
            "name": "latex_userbot",
            "api_id": config.config.API_ID,
            "api_hash": config.config.API_HASH,
            "plugins": dict(root="bot.handlers")
        }

        if config.config.SESSION_STRING:
            client_kwargs["session_string"] = config.config.SESSION_STRING
            
        if config.config.PROXY:
            client_kwargs["proxy"] = config.config.PROXY
            print(f"Использование прокси: {config.config.PROXY['hostname']}:{config.config.PROXY['port']}")
        
        super().__init__(**client_kwargs)