import os
import re
import dotenv
import emoji
from nextcord import Interaction
from Config import PERM


async def missing_perms(interation: Interaction):
    await interation.response.send_message(f"You are missing permissions ({PERM})", ephemeral=True)


def stringify(message):
    text_version = emoji.demojize(message)
    custom_emoji_pattern = r'<:(\w+):\d+>'
    text_version = re.sub(custom_emoji_pattern, r':\1:', text_version)
    return text_version
