from multiprocessing import Process

import nextcord

from nextcord.ext import commands

from Config import *
from api.app import flask_run

placeholer_players = ["LFscrolls", "Phonix75", "RPyro64", "pickle", "Slendersquid360"]

bot = commands.Bot(intents=nextcord.Intents.all())


# Startup
@bot.event
async def on_ready():
    print(f"{bot.user} is now running")


def main():
    cogfiles = [
        f"cogs.{filename[:-3]}" for filename in os.listdir("./cogs/") if filename.endswith(".py")
    ]

    for cogfile in cogfiles:
        try:
            bot.load_extension(cogfile)
        except Exception as err:
            print(err)

    bot.run(token=TOKEN)


if __name__ == "__main__":
    process1 = Process(target=flask_run)
    process2 = Process(target=main)
    process1.start()
    process2.start()
    process1.join()
    process2.join()
