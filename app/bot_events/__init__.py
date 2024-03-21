from .on_ready import on_ready_var
from .on_reaction_add import on_reaction_add_var
from app import bot

@bot.event
async def on_ready():
    on_ready_var.execute(bot.user.name)

@bot.event
async def on_reaction_add(reaction, user):
    await on_reaction_add_var.execute(reaction, user)