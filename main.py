import discord
from discord.ext import commands
import data_files.datafile as packageData

intents = discord.Intents.default()
intents.messages = True  # Ativar a intenção de mensagens

bot = commands.Bot(command_prefix=':', intents=intents)

@bot.event()
async def on_ready():
    print(f'Bot {bot.user.name} está online!')

@bot.command(name="enviar_ultimo")
async def __enviarUltimo(ctx):
    literalMessages = ctx.channel.history(limit=50)
    messages = []
    async for message in literalMessages:
        if message.author.id == ctx.author.id:
            messages.append(message)
    # # Obtendo o histórico de mensagens no canal
    # messages = message.channel.history(limit=50)
    # iteMessages = []
    # async for message in messages :
    #     iteMessages.append(message)

    # # Imprimindo as mensagens no console
    # for msg in iteMessages:
    #     print(f"{msg.author.name}: {msg.content}")
pack = packageData.Datafile_CommuTask()
bot.run(pack.token)
