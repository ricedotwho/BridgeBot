import asyncio

import nextcord
from nextcord import Interaction
from nextcord.ext import commands

from api.API import get_status, send_message_minecraft
from bot.embed_builder import create_embed
from main import GUILD_IDS, ONLINE_COUNT, STATUS, MCPORT, PERM, missing_perms, BRIDGE, stringify

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
        if BRIDGE == '' or interaction.channel_id != int(BRIDGE): return
        if player.lower() in [p.lower() for p in placeholer_players]:
            send_message_minecraft(name=interaction.user.name, message=stringify(message), target=player, mc_port=MCPORT)
            await interaction.response.send_message(f"*You whisper to {player}: {message}*", ephemeral=True)
        else:
            await interaction.response.send_message(f"{player} is not online!", ephemeral=True)


    @commands.Cog.listener()
    async def on_message(self, message):
        if BRIDGE == '' or message.channel.id != int(BRIDGE): return
        if message.author == self.bot.user or message.webhook_id is not None: return
        send_message_minecraft(message.author.name, stringify(message.content), MCPORT)


def setup(bot):
    bot.add_cog(DiscordListener(bot))
