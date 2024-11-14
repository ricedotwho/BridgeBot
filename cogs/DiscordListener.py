import nextcord
from nextcord import Interaction
from nextcord.ext import commands

from api.API import send_message_minecraft, get_online
from Config import *
from utils.Utils import stringify, is_channel_msg, wrong_channel, is_channel


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
        if not is_channel(interaction=interaction, channel_id=getBridge()): await wrong_channel(interaction=interaction, channel_id=getBridge())
        if player.lower() in [p.lower() for p in get_online(getMCPort())]:
            send_message_minecraft(name=interaction.user.name, message=stringify(message), target=player, mc_port=MCPORT)
            await interaction.response.send_message(f"*You whisper to {player}: {message}*", ephemeral=True)
        else:
            await interaction.response.send_message(f"{player} is not online!", ephemeral=True)

    @commands.Cog.listener()
    async def on_message(self, message):
        if not is_channel_msg(message=message, channel_id=getBridge()): return
        if message.author == self.bot.user or message.webhook_id is not None: return
        send_message_minecraft(message.author.name, stringify(message.content), MCPORT)


def setup(bot):
    bot.add_cog(DiscordListener(bot))
