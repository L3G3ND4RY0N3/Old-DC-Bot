import discord
from discord import app_commands
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os as os
import asyncio
from itertools import cycle
import json
#from keep_alive import keep_alive

#Lädt das .env File mit dem Token!
load_dotenv()

#Bot initialiseren und Status Zyklus festlegen
bot = commands.Bot(command_prefix= "$", intents= discord.Intents.all())
bot_status = cycle(["Slapping Juratyp", "Preparing next Slap", "Searching for new Targets"])

#Status Zyklus
@tasks.loop(seconds = 5)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(bot_status)))

#Nachrichten beim Starten des Bots, wie viele Slash Commands gefunden wurden und welche Module geladen sind.
@bot.event
async def on_ready():
    print(f"{bot.user.name} Bot is up and running!")
    change_status.start()
    try: 
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

#Laden der Module aus den cog.py Files
async def load():
    for folder in os.listdir("modules"):
        if os.path.exists(os.path.join("modules", folder, "cog.py")):
            await bot.load_extension(f"modules.{folder}.cog")

#Autoroles für Multiple Server aus Json File
@bot.event
async def on_guild_join(guild):
    with open("modules/Autoroles/json/autoroles.json", "r") as f:
        auto_role = json.load(f)
    
    auto_role[str(guild.id)] = None
                
    with open("modules/Autoroles/json/autoroles.json", "w") as f:
        json.dump(auto_role, f, indent=4)

#Wenn der Bot gekickt wird, löscht den Server aus der Json Datei
@bot.event
async def on_guild_remove(guild):
    with open("modules/Autoroles/json/autoroles.json", "r") as f:
        auto_role = json.load(f)
    
    auto_role.pop(str(guild.id))

    with open("modules/Autoroles/json/autoroles.json", "w") as f:
        json.dump(auto_role, f, indent=4)
                    
#keep_alive()

#Startet den Bot
async def main():
    async with bot:
        await load()
        await bot.start(os.getenv('TOKEN'))

asyncio.run(main())