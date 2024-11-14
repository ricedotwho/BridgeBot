import asyncio

import nextcord
from nextcord import Interaction
from nextcord.ext import commands

from api.API import get_status, get_online
from Config import getOnline, getStatus, getMCPort, GUILD_IDS, getPerms
from utils.Utils import missing_perms, has_role


class ServerListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.running = False

    @nextcord.slash_command(
        name="channelupdater",
        description="Toggles updating",
        guild_ids=GUILD_IDS
    )
    async def func_0001(self, interaction: Interaction):
        if not has_role(interaction, getPerms()):
            await missing_perms(interaction=interaction, role_id=getPerms())
            return
        self.running = not self.running
        if self.running:
            await interaction.response.send_message("Starting", ephemeral=True)
            await self.channel_updater()
        else:
            await interaction.response.send_message("Stopping", ephemeral=True)

    async def channel_updater(self):
        while self.running:
            online: nextcord.VoiceChannel = None if getOnline() == '' else self.bot.get_channel(int(getOnline()))
            status: nextcord.VoiceChannel = None if getStatus() == '' else self.bot.get_channel(int(getStatus()))
            if online is not None:
                await online.edit(name=f"Online: {get_online(getMCPort()).__len__()}", sync_permissions=True)
            if status is not None:
                await status.edit(name=f"Status: {"Online" if get_status(getMCPort()) else "Offline"}", sync_permissions=True)
            await asyncio.sleep(10)


def setup(bot):
    bot.add_cog(ServerListener(bot))
