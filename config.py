import re
from os import getenv
# ------------------------------------
# ------------------------------------
from dotenv import load_dotenv
from pyrogram import filters
# ------------------------------------
# ------------------------------------
load_dotenv()
# ------------------------------------
# -----------------------------------------------------
API_ID = int(getenv("API_ID", "22451491"))
API_HASH = getenv("28e74942125f7e4968398ea651cd417b")
# ------------------------------------------------------
BOT_TOKEN = getenv("6932352695:AAG7ozdXA3jcwTOznBvNvgQWgOG3QH--NZc") 
# -------------------------------------------------------
OWNER_USERNAME = getenv("OWNER_USERNAME","soham_6540")
# --------------------------------------------------------
BOT_USERNAME = getenv("BOT_USERNAME" , "@Teammusic07_bot")
# --------------------------------------------------------
BOT_NAME = getenv("BOT_NAME" , "team music")
# ---------------------------------------------------------
ASSUSERNAME = getenv("ASSUSERNAME" , "MissYumikoo")
# ---------------------------------------------------------

DEEP_API = getenv("DEEP_API", "5163c49d-b696-47f1-8cf9-4801738436dd")
#---------------------------------------------------------------
#---------------------------------------------------------------
MONGO_DB_URI = getenv("mongodb+srv://savitafarkade6540:teamsohammusic@soham.ukgmvta.mongodb.net/", None)
#---------------------------------------------------------------
#---------------------------------------------------------------

# ----------------------------------------------------------------
DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 17000))
# ----------------------------------------------------------------

# ----------------------------------------------------------------
LOGGER_ID = int(getenv("LOGGER_ID", -1001628187842))
# ----------------------------------------------------------------
# ----------------------------------------------------------------
OWNER_ID = int(getenv("OWNER_ID", 6574393060))
# -----------------------------------------------------------------
# -----------------------------------------------------------------

UPSTREAM_REPO = getenv(
    "UPSTREAM_REPO",
    "https://github.com/Sohampro6540/DAXXMUSIC",
)
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "Master")
GIT_TOKEN = getenv(
    "GIT_TOKEN", None
)  # ----------------------------------------------------------------
# -------------------------------------------------------------------
# --------------------------------------------------------------------
# --------------------------------------------------------------------



# ------------------------------------------------------------------------
# -------------------------------------------------------------------------
SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/team_jjk")
SUPPORT_CHAT = getenv("SUPPORT_CHAT💬", "https://t.me/team_jjk")
# ------------------------------------------------------------------------------
# -------------------------------------------------------------------------------







# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------
AUTO_LEAVING_ASSISTANT = getenv("AUTO_LEAVING_ASSISTANT", "True")
AUTO_LEAVE_ASSISTANT_TIME = int(getenv("ASSISTANT_LEAVE_TIME", "9000"))
SONG_DOWNLOAD_DURATION = int(getenv("SONG_DOWNLOAD_DURATION", "9999999"))
SONG_DOWNLOAD_DURATION_LIMIT = int(getenv("SONG_DOWNLOAD_DURATION_LIMIT", "9999999"))
# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------
SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", "19609edb1b9f4ed7be0c8c1342039362")
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", "409e31d3ddd64af08cfcc3b0f064fcbe")
# ----------------------------------------------------------------------------------




# -----------------------------------------------------------------------------------
PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", 25))
# ------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------
TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", "5242880000"))
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", "5242880000"))
# --------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------



# ------------------------------------
# ------------------------------------
# ------------------------------------
# ------------------------------------
STRING1 = getenv("STRING_SESSION", None)
STRING2 = getenv("STRING_SESSION2", None)
STRING3 = getenv("STRING_SESSION3", None)
STRING4 = getenv("STRING_SESSION4", None)
STRING5 = getenv("STRING_SESSION5", None)
STRING6 = getenv("STRING_SESSION6", None)
STRING7 = getenv("STRING_SESSION7", None)
BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}

# ------------------------------------
# ------------------------------------
# ------------------------------------
# ------------------------------------

# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
# ------------------------------------------------------------------------

START_IMG_URL = getenv(
    "START_IMG_URL", "https://telegra.ph/file/67ed7f238db7f033caffa.jpg"
)
PING_IMG_URL = getenv(
    "PING_IMG_URL", "https://telegra.ph/file/f3283959c1201b70e0add.jpg"
)
PLAYLIST_IMG_URL = "https://telegra.ph/file/0f40949b3cdddca29029b.jpg"
STATS_IMG_URL = "https://telegra.ph/file/355bcb1f8e53004655dea.jpg"
TELEGRAM_AUDIO_URL = "https://telegra.ph/file/bfc3a31abbdfa769fc91c.jpg"
TELEGRAM_VIDEO_URL = "https://telegra.ph/file/102d0792234dacfb21f20.jpg"
STREAM_IMG_URL = "https://telegra.ph/file/bfc3a31abbdfa769fc91c.jpg"
SOUNCLOUD_IMG_URL = "https://telegra.ph/file/e95e208fb999d9c265e53.jpg"
YOUTUBE_IMG_URL = "https://telegra.ph/file/bfc3a31abbdfa769fc91c.jpg"
SPOTIFY_ARTIST_IMG_URL = "https://telegra.ph/file/bfc3a31abbdfa769fc91c.jpg"
SPOTIFY_ALBUM_IMG_URL = "https://telegra.ph/file/bfc3a31abbdfa769fc91c.jpg"
SPOTIFY_PLAYLIST_IMG_URL = "https://telegra.ph/file/bfc3a31abbdfa769fc91c.jpg"

# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))


DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# ------------------------------------------------------------------------------
if SUPPORT_CHANNEL:
    if not re.match("(?:http|https)://", SUPPORT_CHANNEL):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHANNEL url is wrong. Please ensure that it starts with https://"
        )

if SUPPORT_CHAT:
    if not re.match("(?:http|https)://", SUPPORT_CHAT):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHAT url is wrong. Please ensure that it starts with https://"
        )
# ---------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------
