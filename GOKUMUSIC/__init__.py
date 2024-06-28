from GOKUMUSIC.core.bot import GOKU
from GOKUMUSIC.core.dir import dirr
from GOKUMUSIC.core.userbot import Userbot
from GOKUMUSIC.music import dbb

from SafoneAPI import SafoneAPI
from .logging import LOGGER

dirr()
dbb()


app = GOKU()
api = SafoneAPI()
userbot = Userbot()


from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()
