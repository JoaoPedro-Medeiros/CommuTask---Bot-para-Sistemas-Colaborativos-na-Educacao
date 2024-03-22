from app import bot
from app.datafiles import DatafileCommuTask

pack = DatafileCommuTask()
bot.run(pack.get_token())