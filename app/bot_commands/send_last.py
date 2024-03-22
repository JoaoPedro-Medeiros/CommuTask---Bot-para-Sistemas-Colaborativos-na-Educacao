from ..staff import FileTransporter
from app import bot
from random import randint
from re import compile
from discord import utils, ChannelType, File, PermissionOverwrite

class SendLastCommand:
    async def execute(self, ctx):
        messages_in_channel = ctx.channel.history(limit=100)
        from_author = await self.__get_messages_from_author(messages_in_channel, ctx.author.id)
        last_message = from_author[1]
        transporter = await self.create_trasporter(last_message.attachments[-1])
        tags_in_message = self.__get_all_tags(last_message.content)
        reviewers = self.__find_reviewers(tags_in_message, ctx)
        try: 
            selected = reviewers[randint(0, len(reviewers) -1)]
        except:
            bot_channel = bot.get_channel(1220238146499907584)
            message = await ctx.author.send(f"Não foi possível enviar o arquivo, {ctx.author.name.capitalize()}! Tente novamente mais tarde, os moderadores desse cargo podem não estar online.")
            await bot_channel.send(f'Foi enviada essa mensagem para {ctx.author.name}: "{message.content}"')
            return
        transporter.set_avaliator_id(selected.id)
        await self.__send_to_avaliator(transporter, ctx)

    async def create_trasporter(self, attachment):
        transporter = FileTransporter()
        await transporter.async_init(attachment)
        return transporter

    async def __get_messages_from_author(self, in_channel, author_id) -> list:
        messages_from_author = []
        async for msg in in_channel:
            if(msg.author.id == author_id) :
                messages_from_author.append(msg)
        return messages_from_author

    def __get_all_tags(self, message_content:str) -> list:
        tag_pattern = compile(r'<@(.*?)>')
        tags = tag_pattern.findall(message_content)
        return tags

    def __find_reviewers(self, tags, ctx) -> list:
        members = []
        role_ids = {int(tag.replace("&", "")) for tag in tags}
        for member in ctx.guild.members:
            if any(role.id in role_ids for role in member.roles):
                members.append(member)
        if any(role.id in role_ids for role in ctx.author.roles):
            members.append(ctx.author)
        return members

    async def __send_to_avaliator(self, filet, ctx):
        avaliator_id = filet.get_avaliator_id()
        nome_canal = str(avaliator_id)
        canal = utils.get(bot.get_all_channels(), name=nome_canal, type=ChannelType.text)
        if not canal:
            await ctx.guild.create_text_channel(nome_canal)
            canal = utils.get(bot.get_all_channels(), name=nome_canal, type=ChannelType.text)
            await self.set_permissions(canal)
        try:
            with open(filet.get_file(), 'rb') as file:
                sended_message = await canal.send(file=File(file))
                await sended_message.add_reaction("✅")
                await sended_message.add_reaction("❌")
            await filet.remove_file()
        except:
            print(f"Permissões insuficientes para enviar mensagens em '{canal.name}', verifique e tente novamente!")
    
    async def set_permissions(self, channel):
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