import os
from discord.ext import commands, tasks
from dotenv import load_dotenv
import asyncpg

load_dotenv()

TOKEN = os.getenv('DISCORD-BOT-TOKEN')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# Create a bot
bot = commands.Bot(command_prefix='.')

# Loading Cogs from other Modules present in Cogs folder
bot.load_extension('bot.cogs.general_commands') # Contains general commands Ex. Ping, hello etc
bot.load_extension('bot.cogs.email_auth_cmnds') # Contains Commands for email authorization Ex. new_auth, token etc
bot.load_extension('bot.cogs.email_read_cmnds') # Contains Commands for reading emails Ex. recent, summery etc

@tasks.loop(seconds=1)
async def printer():
    if CONN.poll():
        data = CONN.recv()
        print(data)

@printer.before_loop
async def before_printer():
    await bot.wait_until_ready()

async def create_db_pool():
    bot.db = await asyncpg.create_pool(database = DB_NAME, user = DB_USER, password = DB_PASSWORD)
    print("Connection To db successful")

def run(conn):
    global CONN
    CONN = conn
    # printer.start()
    bot.loop.run_until_complete(create_db_pool())
    bot.run(TOKEN)

if __name__=="__main__":
    # bot.loop.run_until_complete(create_db_pool())
    bot.run(TOKEN)