import base64
import json
from discord.errors import Forbidden
import re
import html2text
 
def save_or_check_user_info(user,auth=False):
    file = open('user_info.json','r')
    try:
        user_id = json.loads(file.read())
    except:
        user_id={}
    file.close()
    if str(user.id) in user_id.keys():
        if 'token' in user_id[str(user.id)].keys():
            return user_id[str(user.id)]
        else:
            if auth:return user_id[str(user.id)]
            else:return "U/A"
    try:
        user_info = {}
        user_info['name'] = user._user.name
        user_info['discriminator'] = user.discriminator
        user_id[str(user.id)]=user_info
        file = open('user_info.json','w')
        file.seek(0)
        json.dump(user_id,file)
        file.close()
        if 'token' in user_id[str(user.id)].keys():
            return user_id[user.id]
        else:return "U/A"
    except:return False

def save_user(user,id):
    try:
        file = open('user_info.json','r+')
        user_id = json.loads(file.read())
        user_id[str(id)]=user
        file.seek(0)
        file.write(json.dumps(user_id))
        file.close()
        return True
    except Exception as error:
        print("save_user_error=>",error)
        return False

def parse_mail(payld):
    if 'parts' in payld.keys():
        mssg_parts = payld['parts'] # fetching the message parts
        part_one  = mssg_parts[0] # fetching first element of the part
        part_body = part_one['body'] # fetching body of the message
    else:
        part_body = payld['body']
    part_data = part_body['data'] # fetching data from the body
    clean_one = part_data.replace("-","+") # decoding from Base64 to UTF-8
    clean_one = clean_one.replace("_","/") # decoding from Base64 to UTF-8
    mail = clean_one.encode('utf-8')
    mail = base64.b64decode(mail)
    mail = mail.decode('utf-8')
    h = html2text.HTML2Text()
    h.ignore_links=False
    h.ignore_images=True
    h.ignore_tables=False
    mail = h.handle(mail)
    mail = re.sub('\n\n\n+',"\n",str(mail))
    mail = re.sub('   +',' ',mail)
    return mail

async def fetch_users(bot,user):
    user_info = await bot.db.fetchrow("SELECT * FROM users WHERE discord_id = $1",str(user.id))
    if user_info is None:
        return False
    return user_info

async def fetch_users_and_user_token(bot,user):
    user_info = await bot.db.fetchrow("""
        SELECT * FROM users 
        LEFT OUTER JOIN user_token ON (users.discord_id = user_token.fk_user) 
        WHERE users.discord_id = $1;
    """,str(user.id))
    if user_info is None:
        return False
    return user_info

async def check_user(ctx,user,new_auth=False):
    if user:
        if user['token']!=None or new_auth:
            return True
        else:await ctx.channel.send("You are not authorized. Please send '.new_auth' to start the process of authorization")
    else:await ctx.channel.send("Please send '.Hello' in general chat in bot server to start the process of authorization.")
    return False

async def longer_msg(ctx,msg):
    j=0
    i=2000
    while True:
        while msg[i]!=" ":
            i-=1
        else:
            await ctx.author.send(msg[j:i])
        j=i
        if i+2000<len(msg):i+=2000
        else:
            await ctx.author.send(msg[j:])
            break


async def send_embed(ctx, embed):
    """
    Function that handles the sending of embeds
    -> Takes context and embed to send
    - tries to send embed in channel
    - tries to send normal message when that fails
    - tries to send embed private with information about missing permissions
    If this all fails: https://youtu.be/dQw4w9WgXcQ
    """
    try:
        await ctx.send(embed=embed)
    except Forbidden:
        try:
            await ctx.send("Hey, seems like I can't send embeds. Please check my permissions :)")
        except Forbidden:
            await ctx.author.send(
                f"Hey, seems like I can't send any message in {ctx.channel.name} on {ctx.guild.name}\n"
                f"May you inform the server team about this issue? :slight_smile: ", embed=embed)