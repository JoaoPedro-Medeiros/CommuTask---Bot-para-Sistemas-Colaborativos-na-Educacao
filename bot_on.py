from app import bot
from app.datafiles import Datafile_CommuTask

pack = Datafile_CommuTask()
bot.run(pack.getToken())