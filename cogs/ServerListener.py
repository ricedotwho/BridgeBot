import asyncio

import nextcord
from nextcord import Interaction
from nextcord.ext import commands

from api.API import get_status
from bot.embed_builder import create_embed
from main import GUILD_IDS, ONLINE_COUNT, STATUS, MCPORT, PERM, missing_perms

placeholer_players = ["LFscrolls", "Phonix75", "RPyro64", "pickle", "Slendersquid360"]


class ServerListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.updater_running = False


    @nextcord.slash_command(
        name="channelupdater",
        description="Toggles updating",
        guild_ids=GUILD_IDS
    )
    async def func_0001(self, interaction: Interaction):
        if PERM == '' or not any(role.id == PERM for role in interaction.user.roles):
            await missing_perms(interaction)
            return
        self.updater_running = not self.updater_running
        if self.updater_running:
            await interaction.response.send_message("Starting", ephemeral=True)
            await self.channel_updater()
        else:
            await interaction.response.send_message("Stopping", ephemeral=True)

    async def channel_updater(self):
        while self.updater_running:
            #todo: add api request to the server
            online = None if ONLINE_COUNT == '' else self.bot.get_channel(int(ONLINE_COUNT))
            status = None if STATUS == '' else self.bot.get_channel(int(STATUS))
            if online is not None:
                await online.edit(name=f"Online: {len(placeholer_players)}")
            if status is not None:
                await status.edit(name=f"Status: {"Online" if get_status(MCPORT) else "Offline"}")
            await asyncio.sleep(10)


def setup(bot):
    bot.add_cog(ServerListener(bot))
