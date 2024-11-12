import asyncio
import nextcord
from nextcord import Interaction
from nextcord.ext import commands

from api.API import send_message_minecraft
from Config import *
from utils.Utils import stringify

placeholer_players = ["LFscrolls", "Phonix75", "RPyro64", "pickle", "Slendersquid360"]


class DiscordListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.updater_running = False

    @nextcord.slash_command(
        name="message",
        description="Sends a message to the player on the server",
        guild_ids=GUILD_IDS
    )
    async def func_0001(self, interaction: Interaction, player: str, message: str):
        if getBridge() == '' or interaction.channel_id != int(getBridge()): return
        if player.lower() in [p.lower() for p in placeholer_players]:
            send_message_minecraft(name=interaction.user.name, message=stringify(message), target=player, mc_port=MCPORT)
            await interaction.response.send_message(f"*You whisper to {player}: {message}*", ephemeral=True)
        else:
            await interaction.response.send_message(f"{player} is not online!", ephemeral=True)

    @commands.Cog.listener()
    async def on_message(self, message):
        if getBridge() == '' or message.channel.id != int(getBridge()): return
        if message.author == self.bot.user or message.webhook_id is not None: return
        send_message_minecraft(message.author.name, stringify(message.content), MCPORT)


def setup(bot):
    bot.add_cog(DiscordListener(bot))
