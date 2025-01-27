import discord
from discord.ext import commands
from extra_functions import save_or_check_user_info, send_embed

CHANNEL_HELP = """```1. .ping : Bot tells you its latency in ms.
2. .new_auth : Bot sends you a authorization link in your DM.
3. .summery : Bot send general info about your account in your DM.
4. .recent : Bot sends most recent email in your DM.
5. .recent last <N> : Bot sends last "N" recent email in your DM.
6. .search <Keywords> : Bot gives you the result after the search.```"""

class GeneralCommands(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        super().__init__()
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"We have logged in as: {self.bot.user}")

    @commands.Cog.listener()
    async def on_member_join(self,user:discord.User=None):
        new_user = await self.bot.db.fetchrow("SELECT * FROM users WHERE discord_id = $1",str(user.id))
        if new_user is None:
            await self.bot.db.execute("INSERT INTO users (discord_id,name,discriminator) VALUES ($1,$2,$3) RETURNING *",str(user.id),user._user.name,user.discriminator)
        print(f"A member is joined: {user}")

    @commands.command()
    async def ping(self,ctx):
        await ctx.channel.send(f'Bot ping is *{round(self.bot.latency)*1000}ms*')

    @commands.command()
    async def more(self,ctx):
        await ctx.send(CHANNEL_HELP)

    @commands.command()
    async def hello(self,ctx):
        if str(ctx.message.author) != str(ctx.channel).split()[-1]:
            user = await self.bot.db.fetchrow("SELECT * FROM users WHERE discord_id = $1",str(ctx.message.author.id))
            if user is None:
                user = ctx.message.author
                await self.bot.db.execute("INSERT INTO users (discord_id,name,discriminator) VALUES ($1,$2,$3) RETURNING *",str(user.id),user._user.name,user.discriminator)
            embed = discord.Embed(
                title = "Taking first step to save you time",
                description="We will get you latest emails to you without any hassel.\n Type '.new_auth' to start authontication process",
                color = 0xFF5733
            )
            await send_embed(ctx,embed=embed)
        else:
            await ctx.channel.send("Please send '.Hello' in general chat in bot server to start the process of authentication.")

def setup(bot):
    bot.add_cog(GeneralCommands(bot))