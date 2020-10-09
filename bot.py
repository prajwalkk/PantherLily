import logging
import traceback

from discord import Embed, Status, Game, InvalidData
from discord.errors import Forbidden
from discord.ext import commands

from packages.private.settings import Settings
from packages.bot_ext import BotExt


class BotClient(commands.Bot, BotExt):
    def __init__(self, settings, *args, **kwargs):
        super(BotClient, self).__init__(*args, **kwargs) # command_prefix

        self.settings = settings
        # TODO: Set up the db connection here
        self.log = logging.getLogger('root')

        # Set debugging mode
        self.debug = False

    def run(self):
        print('Loading cogs...')
        for cog in self.settings.enabled_cogs:
            try:
                self.load_extension(cog)
            except Exception as error:
                self.log.error(error, exc_info=True)

        print('Cogs loaded, establishing connection')
        super().run(self.settings.bot_config['bot_token'], reconnect=True)

    async def on_ready(self):
        print("Connected")
        self.log.debug('Established connection')
        await self.change_presence(status=Status.online, activity=Game(name=self.settings.bot_config['version']))

    async def on_resume(self):
        self.log.info('Resuming connection...')

    async def on_command(self, ctx):
        await ctx.message.channel.trigger_typing()


    async def on_command_error(self, ctx, error):
        if self.debug:
            exc = ''.join(
                traceback.format_exception(type(error), error, error.__traceback__, chain=True))

            await self.embed_print(ctx, title='DEBUG ENABLED', description=f'{exc}',
                                   codeblock=True, color='warning')

        # Catch all errors within command logic
        if isinstance(error, commands.CommandInvokeError):
            original = error.original
            # Catch errors such as roles not found
            if isinstance(original, InvalidData):
                await self.embed_print(ctx, title='INVALID OPERATION', color='error',
                                       description=original.args[0])
                return

            # Catch permission issues
            elif isinstance(original, Forbidden):
                await self.embed_print(ctx, title='FORBIDDEN', color='error',
                                       description='Even with proper permissions, the target user must be lower in the '
                                                   'role hierarchy of this bot.')
                return

        # Catch command.Check errors
        if isinstance(error, commands.CheckFailure):
            try:
                if error.args[0] == 'Not owner':
                    await self.embed_print(ctx, title='COMMAND FORBIDDEN', color='error',
                                           description='Only Doobie can run this command')
                    return
            except:
                pass
            await self.embed_print(ctx, title='COMMAND FORBIDDEN', color='error',
                                   description='Only `CoC Leadership` are permitted to use this command')
            return

        # Catch all
        await self.embed_print(ctx, title='COMMAND ERROR',
                               description=str(error), color='error')
