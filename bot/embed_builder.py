from nextcord import Embed, Colour

CREDITS = "Made by @rice.who"


def create_embed(title: str = "", body: str = "", footer: str = "", url: str = "", credits: bool = False) -> Embed:
    embed = Embed(
        colour=Colour.dark_purple(),
        title=title,
        description=body,
        url=url
    )
    if footer != "":
        footer += "\n"
    embed.set_footer(text=f"{footer} {f"\n{CREDITS}" if credits else ""}")
    return embed
