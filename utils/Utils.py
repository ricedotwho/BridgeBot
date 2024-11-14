import re
import emoji
from nextcord import Interaction


def has_role(interaction: Interaction, role_id) -> bool:
    if role_id == '' or not any(role.id == role_id for role in interaction.user.roles):
        return False
    return True


def is_channel(interaction: Interaction, channel_id):
    if channel_id == '' or interaction.channel_id != int(channel_id): return


def is_channel_msg(message, channel_id):
    if channel_id == '' or message.channel.id != int(channel_id):
        return False
    return True


async def missing_perms(interaction: Interaction, role_id=None):
    if role_id is None:
        await interaction.response.send_message(f"You are missing permissions!", ephemeral=True)
    else:
        await interaction.response.send_message(f"You are missing permissions! ({role_id})", ephemeral=True)


async def wrong_channel(interaction: Interaction, channel_id=None):
    if channel_id is None:
        await interaction.response.send_message(f"You are missing permissions!", ephemeral=True)
    else:
        await interaction.response.send_message(f"You are missing permissions! (#{channel_id})", ephemeral=True)


def stringify(message):
    text_version = emoji.demojize(message)
    custom_emoji_pattern = r'<:(\w+):\d+>'
    text_version = re.sub(custom_emoji_pattern, r':\1:', text_version)
    return text_version
