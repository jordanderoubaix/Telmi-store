from dotenv import load_dotenv
import os

load_dotenv()
class Settings():
    SHARED_DIRECTORY_PATH: str = os.getenv("SHARED_DIRECTORY_PATH", "/mnt/nfs/telmiLibrary")
    SHARED_DIRECTORY_USERNAME: str = os.getenv("SHARED_DIRECTORY_USERNAME", "telmi")
    SHARED_DIRECTORY_PASSWORD: str = os.getenv("SHARED_DIRECTORY_PASSWORD", "telmipassword")
    TARGET_URL: str
    BANNER_IMAGE: str = os.getenv("BANNER_IMAGE", "https://raw.githubusercontent.com/histoires-pour-tous/.github/main/profile/banner-telmi.jpg")
    BANNER_LINK: str = os.getenv("BANNER_LINK", "https://monurl.ca/lunii.creations/")
    BANNER_BACKGROUND: str = os.getenv("BANNER_BACKGROUND", "#016673")
    LIBRARY_LINK: str = os.getenv("LIBRARY_LINK", "http://link.to.library/telmilib")


settings = Settings()
