import discord
from discord.ext import commands
from gmail.gmail_cmnds import service
from extra_functions import send_embed, save_or_check_user_info,check_user

class SendEmails(commands.Cog):
    def __init__(self,bot) -> None:
        self.bot = bot
        super().__init__()

    @commands.command()
    async def sendmail(self,ctx,mail):
        user = save_or_check_user_info(ctx.message.author)
        if await check_user(ctx,user):
            service_obj = service(user['token'])
            message = service_obj.create_message(mail)

def setup(bot):
    bot.add_cog(SendEmails(bot))