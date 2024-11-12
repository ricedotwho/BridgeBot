import nextcord
from nextcord import Interaction
from nextcord.ext import commands

from bot.embed_builder import create_embed
from main import GUILD_IDS

placeholer_players = ["LFscrolls", "Phonix75", "RPyro64", "pickle", "Slendersquid360"]


class Online(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="online",
        description="Shows all online players",
        guild_ids=GUILD_IDS
    )
    async def func_0005(self, interaction: Interaction):
        player_string = f""
        for nextp, p in enumerate(placeholer_players):
            player_string += f"{p}"
            if nextp is not None:
                player_string += "\n"

        await interaction.response.send_message(embed=create_embed(
            f"Online Players: **{len(placeholer_players)}**",
            body=f"{player_string}"))


def setup(bot):
    bot.add_cog(Online(bot))
