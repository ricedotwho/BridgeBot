import asyncio
import json
import os
import re
from multiprocessing import Process

import emoji
import nextcord
from nextcord import Interaction

from api.API import get_status, send_message_minecraft
import dotenv
from nextcord.ext import commands
#from discord.ext import commands
import discord

from api.API import send_message_discord, create_message
from api.app import flask_run
#from bot.embed_builder import create_embed

env_dir: str = str(os.path.dirname(os.path.abspath(__file__))) + "/.env"

dotenv.load_dotenv()
TOKEN: str = os.getenv('DISCORD_TOKEN')
GUILD_IDS: list = json.loads(os.getenv('GUILD_IDS'))
GUILD_IDS = [int(guild_id) for guild_id in GUILD_IDS]
STATUS: str = os.getenv('STATUS_ID')
ONLINE_COUNT: int = int(os.getenv('ONLINECOUNT_ID'))
BRIDGE: str = os.getenv('BRIDGE_ID')
PERM: int = int(os.getenv('PERM_ROLE_ID'))
MCPORT: int = int(os.getenv('MC_PORT'))
updater_running = False

placeholer_players = ["LFscrolls", "Phonix75", "RPyro64", "pickle", "Slendersquid360"]

bot = commands.Bot(intents=nextcord.Intents.all())


# Startup
@bot.event
async def on_ready():
    print(f"{bot.user} is now running")
    #send_message_discord(create_message("Started!"), False)


# @bot.event
# async def on_message(message):
#     if BRIDGE == '' or message.channel.id != int(BRIDGE): return
#     if message.author == bot.user or message.webhook_id is not None: return
#     send_message_minecraft(message.author.name, stringify(message.content), MCPORT)


# @bot.slash_command(
#     name="message",
#     description="Sends a message to the player on the server",
#     guild_ids=GUILD_IDS
# )
# async def func_0001(ctx, player: str, message: str):
#     if BRIDGE == '' or ctx.channel_id != int(BRIDGE): return
#     if player.lower() in [p.lower() for p in placeholer_players]:
#         send_message_minecraft(name=ctx.author.name, message=stringify(message), target=player, mc_port=MCPORT)
#         await ctx.respond(f"*You whisper to {player}: {message}*", ephemeral=True)
#     else:
#         await ctx.respond(f"{player} is not online!", ephemeral=True)
#
#
# @bot.slash_command(
#     name="channelupdater",
#     description="Toggles updating",
#     guild_ids=GUILD_IDS
# )
# async def func_0002(ctx):
#     if PERM == '' or not any(role.id == PERM for role in ctx.author.roles):
#         await missing_perms(ctx)
#         return
#     global updater_running
#     updater_running = not updater_running
#     if updater_running:
#         await ctx.respond("Starting", ephemeral=True)
#         await channel_updater()
#     else:
#         await ctx.respond("Stopping", ephemeral=True)
#
#
# @bot.slash_command(
#     name="setbridge",
#     description="Sends a message to the player on the server",
#     guild_ids=GUILD_IDS
# )
# async def func_0003(ctx):
#     if PERM == '' or not any(role.id == PERM for role in ctx.author.roles):
#         await missing_perms(ctx)
#         return
#     set_env("BRIDGE_ID", str(ctx.channel_id))
#     global BRIDGE
#     BRIDGE = str(ctx.channel_id)
#     await ctx.respond(f"Set the bridge channel to: {str(ctx.channel)} ({str(ctx.channel_id)}) ({BRIDGE})",
#                       ephemeral=True)
#
#
# @bot.slash_command(
#     name="setup",
#     description="Sends a message to the player on the server",
#     guild_ids=GUILD_IDS
# )
# async def func_0004(ctx, role_id: str = None, status_id: str = None, online_id: str = None,
#                     bridge_id: str = None, mc_port: str = None, mc_url: str = None):
#     global PERM
#     if PERM != '' and not any(role.id == PERM for role in ctx.author.roles):
#         await missing_perms(ctx)
#         return
#     if role_id is not None:
#         set_env("PERM_ROLE_ID", role_id)
#         PERM = int(role_id)
#     if status_id is not None:
#         set_env("STATUS_ID", status_id)
#         global STATUS
#         STATUS = status_id
#     if online_id is not None:
#         set_env("ONLINECOUNT_ID", online_id)
#         global ONLINE_COUNT
#         ONLINE_COUNT = int(online_id)
#     if bridge_id is not None:
#         set_env("BRIDGE_ID", bridge_id)
#         global BRIDGE
#         BRIDGE = bridge_id
#     if mc_port is not None:
#         set_env("MC_PORT", mc_port)
#         global MCPORT
#         MCPORT = mc_port
#     await ctx.respond(
#         embed=create_embed(
#             title="**Setup Complete!**",
#             body=f"{f"Role ID: {role_id}\n" if role_id is not None else ""}{f"Status ID: {status_id}\n" if status_id is not None else ""}{f"Online ID: {online_id}\n" if online_id is not None else ""}{f"Bridge ID: {bridge_id}\n" if bridge_id is not None else ""}"
#         ), ephemeral=True)


async def missing_perms(interation: Interaction):
    await interation.response.send_message(f"You are missing permissions ({PERM})", ephemeral=True)


def stringify(message):
    text_version = emoji.demojize(message)
    custom_emoji_pattern = r'<:(\w+):\d+>'
    text_version = re.sub(custom_emoji_pattern, r':\1:', text_version)
    return text_version


def set_env(key: str, value: str):
    dotenv.set_key(dotenv_path=env_dir, key_to_set=key, value_to_set=value)


async def channel_updater():
    while updater_running:
        #todo: add api request to the server
        online = None if ONLINE_COUNT == '' else bot.get_channel(int(ONLINE_COUNT))
        status = None if STATUS == '' else bot.get_channel(int(STATUS))
        if online is not None:
            await online.edit(name=f"Online: {len(placeholer_players)}")
        if status is not None:
            await status.edit(name=f"Status: {"Online" if get_status(MCPORT) else "Offline"}")
        await asyncio.sleep(10)


cogfiles = [
    f"cogs.{filename[:-3]}" for filename in os.listdir("./cogs/") if filename.endswith(".py")
]

for cogfile in cogfiles:
    try:
        bot.load_extension(cogfile)
    except Exception as err:
        print(err)



def main():
    bot.run(token=TOKEN)


if __name__ == "__main__":
    process1 = Process(target=flask_run)
    process2 = Process(target=main)
    process1.start()
    process2.start()
    process1.join()
    process2.join()
