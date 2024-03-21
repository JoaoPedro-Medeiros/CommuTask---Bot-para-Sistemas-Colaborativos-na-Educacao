import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=">>", intents=intents)

import app.bot_commands as c
import app.bot_events as e