import uuid

import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from bot.embed_builder import create_embed
from Config import *
from utils.Utils import missing_perms, has_role


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.updater_running = False

    @nextcord.slash_command(
        name="setbridge",
        description="Sets the current channel to the bridge channel",
        guild_ids=GUILD_IDS
    )
    async def func_0001(self, interaction: Interaction):
        if not has_role(interaction, getPerms()):
            await missing_perms(interaction)
            return
        changeBridge(str(interaction.channel_id))
        await interaction.response.send_message(
            f"Set the bridge channel to: {str(interaction.channel)} ({str(interaction.channel_id)} {getBridge()})", ephemeral=True)

    @nextcord.slash_command(
        name="setup",
        description="Sends a message to the player on the server",
        guild_ids=GUILD_IDS
    )
    async def func_0002(self, interaction: Interaction,
                        role_id: str = None,
                        status_id: str = None,
                        online_id: str = None,
                        bridge_id: str = None,
                        mc_port: str = None,
                        api_key: str = None,
                        avatar_link: str = None,
                        whitelist_id: str = None):
        if not has_role(interaction, getPerms()):
            await missing_perms(interaction)
            return
        if role_id is not None:
            changePerms(int(role_id))
        if status_id is not None:
            changeStatus(status_id)
        if online_id is not None:
            changeOnlineCount(int(online_id))
        if bridge_id is not None:
            changeBridge(bridge_id)
        if mc_port is not None:
            changeMCPort(int(mc_port))
        if api_key is not None:
            changeApiKey(api_key)
        if avatar_link is not None:
            changeAvatar(avatar_link)
        if whitelist_id is not None:
            changeWhitelistId(whitelist_id)
        await interaction.response.send_message(
            embed=create_embed(
                title="**Setup Complete!**",
                body=f"{f"Role ID: {role_id}\n" if role_id is not None else ""}"
                     f"{f"Status ID: {status_id}\n" if status_id is not None else ""}"
                     f"{f"Online ID: {online_id}\n" if online_id is not None else ""}"
                     f"{f"Bridge ID: {bridge_id}\n" if bridge_id is not None else ""}"
                     f"{f"MC Port ID: {mc_port}\n" if mc_port is not None else ""}"
                     f"{f"Api-Key: {api_key}\n" if api_key is not None else ""}"
                     f"{f"Avatar Link: {avatar_link}\n" if avatar_link is not None else ""}"
                     f"{f"Whitelist role ID: {whitelist_id}\n" if whitelist_id is not None else ""}"
            ),
            ephemeral=True)

    @nextcord.slash_command(
        name="genuuid",
        description="Generates a random UUID",
        guild_ids=GUILD_IDS
    )
    async def func_0003(self, interaction: Interaction):
        if not has_role(interaction, getPerms()):
            await missing_perms(interaction)
            return
        uid = uuid.uuid4()
        await interaction.response.send_message(
            f"UUID: {uid}", ephemeral=True)


def setup(bot):
    bot.add_cog(Admin(bot))
