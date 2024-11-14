import nextcord
from nextcord import Interaction
from nextcord.ext import commands

from Config import getMCPort, GUILD_IDS, getWhitelistId, getPerms
from api.API import send_command_minecraft
from utils.Utils import missing_perms, has_role


class ServerCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="whitelistadd",
        description="Add a player to the server whitelist",
        guild_ids=GUILD_IDS
    )
    async def func_0001(self, interaction: Interaction, username: str):
        if not has_role(interaction, getPerms()) or not has_role(interaction, getWhitelistId()):
            await missing_perms(interaction=interaction, role_id=getWhitelistId())
            return
        send_command_minecraft(command=f"whitelist add {username}", mc_port=getMCPort())
        await interaction.response.send_message(f"Added {username} to the whitelist!", ephemeral=True)

    @nextcord.slash_command(
        name="whitelistremove",
        description="Remove a player to the server whitelist",
        guild_ids=GUILD_IDS
    )
    async def func_0002(self, interaction: Interaction, username: str):
        if not has_role(interaction, getPerms()) or not has_role(interaction, getWhitelistId()):
            await missing_perms(interaction=interaction, role_id=getWhitelistId())
            return
        send_command_minecraft(command=f"whitelist remove {username}", mc_port=getMCPort())
        await interaction.response.send_message(f"Removed {username} from the whitelist!", ephemeral=True)

    @nextcord.slash_command(
        name="bridgecommand",
        description="Runs a bridge command on the server side",
        guild_ids=GUILD_IDS
    )
    async def func_0003(self, interaction: Interaction, args: str):
        if not has_role(interaction, getPerms()):
            await missing_perms(interaction=interaction, role_id=getPerms())
            return
        send_command_minecraft(command=f"b {args}", mc_port=getMCPort())
        await interaction.response.send_message(f"Ran /b {args}", ephemeral=True)

    @nextcord.slash_command(
        name="execcommand",
        description="Runs command on the server side",
        guild_ids=GUILD_IDS
    )
    async def func_0004(self, interaction: Interaction, args: str):
        if not has_role(interaction, getPerms()):
            await missing_perms(interaction=interaction, role_id=getPerms())
            return
        send_command_minecraft(command=f"{args}", mc_port=getMCPort())
        await interaction.response.send_message(f"Ran {args}", ephemeral=True)


def setup(bot):
    bot.add_cog(ServerCommands(bot))
