from app import bot
from ..staff import FileTransporter
import os
# API do Google Drive (Teria que consumir a API do Google Drive, então ainda não está sendo utilizado)
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.auth.exceptions import RefreshError
from google.auth import exceptions
#######################################################


class OnReactionAddEvent:

    def __init__(self):
        self.__reacted = False

    async def execute(self, reaction, user):
        if await self.initialVerifications(reaction, user):
            return
        
        if str(reaction.emoji) == '✅':
            file = FileTransporter()
            try: await file.asyncInit(reaction.message.attachments[0])
            except: return
            await self.sendToDrive(file.getFile())
        await reaction.message.delete()

    async def initialVerifications(self, reaction, user):
        if user.bot:
            return True
        
        if reaction.message.channel.name != str(user.id) and not user.guild_permissions.administrator: 
            return True
    
    async def sendToDrive(self, path_to_file):
        print("Enviado para o Drive!") #TODO Aqui seria o envio para o drive
        pass

on_reaction_add_var = OnReactionAddEvent()