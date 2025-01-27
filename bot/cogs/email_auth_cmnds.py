import os
import discord
import json
from discord.ext import commands
from gmail.gmail_cmnds import service
from gmail.gmail_auth import get_authorization_url,get_credentials
from extra_functions import check_user,save_user,fetch_users,fetch_users_and_user_token

class Authorization(commands.Cog):
    def __init__(self,bot) -> None:
        self.bot = bot
        super().__init__()

    @commands.command(aliases=['new_auth'])
    async def new_authorization(self, ctx):
        user = await fetch_users_and_user_token(self.bot,ctx.message.author)
        if await check_user(ctx,user,new_auth=True):
            if user['token'] is None:
                url = get_authorization_url()
                url_embed = discord.Embed(
                    title = "Click to go to verification page",
                    url=f"{url}",
                    description = 'To authorize type => .token <YOUR_TOKEN>  here only .\n Warning do not share your auth token.',
                    color=0xFF5733
                )
                await ctx.channel.send(embed=url_embed)
            else:
                await ctx.channel.send("You have already authorized 1 gmail account.")

    @commands.command()
    async def token(self, ctx,token):
        user = await fetch_users_and_user_token(self.bot,ctx.message.author)
        if await check_user(ctx,user,new_auth=True):
            if user['token'] is None:
                await ctx.channel.send(f"Your authorization token is processing.")
                cred=get_credentials(authorization_code=token)
                if cred != None:
                    token = json.loads(cred.to_json())
                    email = await self.get_email(token)
                    category_id = await self.user_setup(ctx,email)
                    details = await self.bot.db.fetchrow("SELECT * FROM user_token WHERE email = $1",email)
                    if details is not None:
                        await ctx.channel.send(f"Sorry {email} is already authorized")
                    else:
                        try:
                            # SELECT * FROM users INNER JOIN user_token ON (users.discord_id = user_token.email) WHERE users.name = 'THuNdErBoLt';
                            await self.bot.db.execute("""
                            INSERT INTO user_token (email,token,category_id,fk_user) VALUES
                            ($1,$2,$3,(SELECT discord_id FROM users WHERE discord_id = $4))
                            """,email,str(token),str(category_id),str(ctx.message.author.id))
                            success=True
                        except Exception as e:
                            success=False
                        if success:
                            await ctx.channel.send(f"Congratulations {ctx.message.author},You have verified successfully. Type '.more' for more help")
                        else:
                            await ctx.channel.send(f"Sorry something went wrong.")
                else:
                    await ctx.channel.send("There is something wrong with your token. Please check again")
            else:
                await ctx.channel.send("You have already authorized 1 gmail account.")

    async def get_email(self,token):
        service_obj = service(token)
        profile = service_obj.get_profile(for_user_token=True)
        return profile['emailAddress']

    async def user_setup(self,ctx,email):
        """GENERAL,INBOX,SENT,DRAFTS,STARRED,SPAM,iMPORTANT"""
        guild = ctx.message.guild
        gmail_tabs = ["COMPOSE","INBOX","SENT","DRAFTS","STARRED","SPAM","IMPORTANT"]
        have_email_category=False
        category_id = None
        for category in guild.categories:
            if category.name==email:
                have_email_category=True
                email_category = category
                category_id=category.id
        if not have_email_category:
            await guild.create_category(email)
            for category in guild.categories:
                if category.name==email:
                    email_category = category
                    category_id=category.id
        for text_channel in email_category.channels:
            if text_channel.name.upper() in gmail_tabs:gmail_tabs.remove(text_channel.name.upper())
        for tab in gmail_tabs:
            await guild.create_text_channel(tab,category=email_category)
        return category_id

def setup(bot):
    bot.add_cog(Authorization(bot))