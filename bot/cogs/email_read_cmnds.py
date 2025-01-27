import discord
from discord.ext import commands
from gmail.gmail_cmnds import service
from extra_functions import longer_msg, send_embed, fetch_users_and_user_token,check_user
import json

class ReadEmails(commands.Cog):
    def __init__(self,bot) -> None:
        self.bot = bot
        super().__init__()

    @commands.command()
    async def summary(self,ctx):
        user = await fetch_users_and_user_token(self.bot,ctx.message.author)
        if await check_user(ctx,user):
            token = json.loads(user['token'].replace("'",'"'))
            service_obj = service(token)
            summary=service_obj.get_profile()
            summery_embed = discord.Embed(
                title = "Your account summary",
                description = summary,
                color = discord.Color.blue()
            )
            await send_embed(ctx,embed=summery_embed)

    @commands.group(name='recent', invoke_without_command=True)
    async def recent(self, ctx):
        user = await fetch_users_and_user_token(self.bot,ctx.message.author)
        if await check_user(ctx,user):
            token = json.loads(user['token'].replace("'",'"'))
            service_obj = service(token)
            mail = service_obj.get_emails()
            for i in mail:
                mail_content = service_obj.get_message(i['id'],True)
                message=''
                try:
                    for i in mail_content.keys():
                        if 'body'==i:
                            continue
                        message+=f"\n[{i}]: {mail_content[i]}"
                    await ctx.channel.send(f"```ini\n{message}```")
                    if "body" in mail_content.keys():
                        if len(mail_content['body'])<2000:
                            await ctx.channel.send(f"{mail_content['body']}")
                        else:await longer_msg(ctx,mail_content['body'])
                except Exception as e:
                    print(e)

    @recent.command(name='last')
    async def last(self,ctx,amount=1):
        user = await fetch_users_and_user_token(self.bot,ctx.message.author)
        if await check_user(ctx,user):
            token = json.loads(user['token'].replace("'",'"'))
            service_obj = service(token)
            mail = service_obj.get_emails(amount)
            for i in mail:
                mail_content = service_obj.get_message(i['id'])
                message=''
                for i in mail_content.keys():
                    message+=f"\n[{i}]: {mail_content[i]}"
                await ctx.channel.send(f"```ini\n{message}```")
        
    @commands.command()
    async def search(self,ctx,search_string):
        user = await fetch_users_and_user_token(self.bot,ctx.message.author)
        if await check_user(ctx,user):
            token = json.loads(user['token'].replace("'",'"'))
            service_obj = service(token)
            mail = service_obj.search_email(search_string)
            if mail['resultSizeEstimate']!=0:
                for i in mail['messages']:
                    mail_content = service_obj.get_message(i['id'],True)
                    message=''
                    for i in mail_content.keys():
                        message+=f"\n[{i}]: {mail_content[i]}"
                    await ctx.channel.send(f"```ini\n{message}```")
            else:
                await ctx.channel.send("Sorry No Results Found")


def setup(bot):
    bot.add_cog(ReadEmails(bot))