from dotenv import load_dotenv
import os
import logging
import secrets

load_dotenv()

class Settings():
    SHARED_DIRECTORY_PATH: str = os.getenv("SHARED_DIRECTORY_PATH", "/mnt/nfs/telmiLibrary")
    SHARED_DIRECTORY_USERNAME: str = os.getenv("SHARED_DIRECTORY_USERNAME", "telmi")
    SHARED_DIRECTORY_PASSWORD: str = os.getenv("SHARED_DIRECTORY_PASSWORD", "telmipassword")
    TARGET_URL: str
    BANNER_IMAGE: str = os.getenv("BANNER_IMAGE", "https://raw.githubusercontent.com/Seph29/Telmi-store/main/custom-store.png")
    BANNER_LINK: str = os.getenv("BANNER_LINK", "https://monurl.ca/lunii.creations/")
    BANNER_BACKGROUND: str = os.getenv("BANNER_BACKGROUND", "#000000")
    LIBRARY_LINK: str = os.getenv("LIBRARY_LINK", "http://#")
    API_KEY: str = os.getenv("API_KEY", None)
    if API_KEY is None:
        API_KEY = secrets.token_urlsafe(32)

settings = Settings()
