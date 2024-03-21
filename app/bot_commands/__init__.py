from .send_last import send_last_var
from app import bot

@bot.command("enviar_ultimo")
async def enviar_ultimo(ctx):
    await send_last_var.execute(ctx)