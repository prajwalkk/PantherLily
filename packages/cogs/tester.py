from discord.ext import commands
from coc import utils, NotFound
from discord import Embed
#from packages.cogs.utils import embed_print
from packages.cogs.utils.utils import parse_args


class Tester(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def ping(self, ctx):
        await self.bot.embed_print(ctx=ctx, description='ponnnnnnnnng')

    @commands.command()
    async def test(self, ctx):
        await self.bot.embed_print(ctx, self.bot.settings.emojis['add'])
        await self.bot.embed_print(ctx, self.bot.settings.emojis['delete'])
        await self.bot.embed_print(ctx, self.bot.settings.emojis['complete'])
        await self.bot.embed_print(ctx, self.bot.settings.emojis['check'])
        await self.bot.embed_print(ctx, self.bot.settings.emojis['reset'])
        await self.bot.embed_print(ctx, self.bot.settings.emojis['approved'])
        await self.bot.embed_print(ctx, self.bot.settings.emojis['cancel'])


    @commands.command()
    async def get_user(self, ctx, *, arg_string):
        arg_dict = {
            'coc_tag': {
                'flags': ['--clash', '-c'],
                'required': True
            },
            'discord_id': {
                'flags': ['--discord', '-d'],
                'required': True,
                'type': 'int'
            },
        }
        args = await parse_args(ctx, self.bot.settings, arg_dict, arg_string)
        if not args:
            return

        async with self.bot.pool.acquire() as con:
            row = await con.fetchrow('select * from discord_user where discord_id = $1', args.discord_id)

        print(row)


def setup(bot):
    bot.add_cog(Tester(bot))