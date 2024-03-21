from ..staff import FileTransporter
from app import bot
from random import randint
import asyncio
import re
from discord import utils, ChannelType, File, PermissionOverwrite

class SendLastCommand:
    async def execute(self, ctx):
        messagesInChannel = ctx.channel.history(limit=100)
        fromAuthor = await self.__getMessagesFromAuthor(messagesInChannel, ctx.author.id)
        lastMessage = fromAuthor[1]
        transporter = await self.createTrasporter(lastMessage.attachments[-1])
        tagsInMessage = self.__getAllTags(lastMessage.content)
        reviewers = self.__findReviewers(tagsInMessage, ctx)
        print(reviewers)
        try: 
            selected = reviewers[randint(0, len(reviewers) -1)]
        except:
            bot_channel = bot.get_channel(1220238146499907584)
            message = await ctx.author.send(f"Não foi possível enviar o arquivo, {ctx.author.name.capitalize()}! Tente novamente mais tarde, os moderadores desse cargo podem não estar online.")
            await bot_channel.send(f'Foi enviada essa mensagem para {ctx.author.name}: "{message.content}"')
            return
        transporter.setAvaliatorId(selected.id)
        await self.__sendToAvaliator(transporter, ctx)

    async def createTrasporter(self, attachment):
        transporter = FileTransporter()
        await transporter.asyncInit(attachment)
        return transporter

    async def __getMessagesFromAuthor(self, inChannel, authorId) -> list:
        messageFromAuthor = []
        async for msg in inChannel:
            if(msg.author.id == authorId) :
                messageFromAuthor.append(msg)
        return messageFromAuthor

    def __getAllTags(self, message_content:str) -> list:
        tag_pattern = re.compile(r'<@(.*?)>')
        tags = tag_pattern.findall(message_content)
        return tags

    def __findReviewers(self, tags, ctx) -> list:
        members = []
        # print(members)
        role_ids = {int(tag.replace("&", "")) for tag in tags}
        # print(role_ids)
        for member in ctx.guild.members:
            # print(ctx.guild.members)
            if any(role.id in role_ids for role in member.roles):
                # print(any(role.id in role_ids for role in member.roles))
                members.append(member)
        if any(role.id in role_ids for role in ctx.author.roles):
            members.append(ctx.author)
        return members

    async def __sendToAvaliator(self, filet, ctx):
        avaliator_id = filet.getAvaliatorId()
        nome_canal = str(avaliator_id)
        canal = utils.get(bot.get_all_channels(), name=nome_canal, type=ChannelType.text)
        if not canal:
            await ctx.guild.create_text_channel(nome_canal)
            canal = utils.get(bot.get_all_channels(), name=nome_canal, type=ChannelType.text)
            await self.setPermissions(canal)
        try:
            with open(filet.getFile(), 'rb') as file:
                sended_message = await canal.send(file=File(file))
                await sended_message.add_reaction("✅")
                await sended_message.add_reaction("❌")
            await filet.removeFile()
        except:
            print(f"Permissões insuficientes para enviar mensagens em '{canal.name}', verifique e tente novamente!")
    
    async def setPermissions(self, channel):
        overwrite = PermissionOverwrite()
        overwrite.read_messages = True
        overwrite.read_message_history = True
        overwrite.send_messages = True
        owner_member = channel.guild.get_member(channel.guild.owner_id)
        if owner_member is None:
            owner_member = await channel.guild.fetch_member(channel.guild.owner_id)
        await channel.set_permissions(owner_member, overwrite=overwrite)
        for role in channel.guild.roles:
            if role.permissions.administrator:
                await channel.set_permissions(role, overwrite=overwrite)

send_last_var = SendLastCommand()