import os
import shutil
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

# Bot Token (User will provide or fill in .env)
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()

# Admin IDs (comma separated integers in .env, e.g. "12345678,87654321")
ADMIN_RAW = os.getenv("ADMINS", "")
ADMINS = [int(x.strip()) for x in ADMIN_RAW.split(",") if x.strip().isdigit()]

# Database path (supports custom volume path on server)
DB_PATH = os.getenv("DB_PATH", str(BASE_DIR / "bot.db"))

# Downloads & Temp directories
TEMP_DIR = BASE_DIR / "downloads"
TEMP_DIR.mkdir(parents=True, exist_ok=True)

# Cookies file path (supports cookies.txt or YOUTUBE_COOKIES env var on server)
COOKIES_PATH = BASE_DIR / "cookies.txt"
env_cookies = os.getenv("YOUTUBE_COOKIES", "").strip()
if env_cookies and not COOKIES_PATH.exists():
    try:
        COOKIES_PATH.write_text(env_cookies, encoding="utf-8")
    except Exception:
        pass

# Robust FFmpeg path: prefers system ffmpeg in Linux/Docker, falls back to imageio-ffmpeg
system_ffmpeg = shutil.which("ffmpeg")
if system_ffmpeg:
    FFMPEG_PATH = system_ffmpeg
else:
    try:
        import imageio_ffmpeg
        FFMPEG_PATH = imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        FFMPEG_PATH = "ffmpeg"

# Bot Information
BOT_NAME = os.getenv("BOT_NAME", "HitMusic Bot")
BOT_USERNAME = os.getenv("BOT_USERNAME", "my_hitmusic_bot")
SUPPORT_USERNAME = os.getenv("SUPPORT_USERNAME", "")

# Cloud Web Port for Render / Railway / Koyeb healthcheck (if running as Web service)
PORT = os.getenv("PORT", "").strip()

# Gemini AI API Key for smart music understanding and lyrics recognition
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

