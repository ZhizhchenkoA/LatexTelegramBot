import os
from dotenv import load_dotenv

load_dotenv()

def get_proxy():
    """Читает настройки прокси из .env. Возвращает None, если хост не указан."""
    hostname = os.getenv("PROXY_HOSTNAME")
    if not hostname:
        return None
    
    proxy = {
        "scheme": os.getenv("PROXY_SCHEME", "socks5"), # socks5 или http
        "hostname": hostname,
        "port": int(os.getenv("PROXY_PORT", 10808)),
    }
    
    username = os.getenv("PROXY_USERNAME")
    password = os.getenv("PROXY_PASSWORD")
    if username: proxy["username"] = username
    if password: proxy["password"] = password
        
    return proxy

class Settings:
    API_ID: int = int(os.getenv("API_ID", 0))
    API_HASH: str = os.getenv("API_HASH", "")
    SESSION_STRING: str = os.getenv("SESSION_STRING", None)
    PREFIX: str = os.getenv("PREFIX", ".")
    PROXY: dict = get_proxy()

config = Settings()