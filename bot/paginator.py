import discord


class PaginatorView(discord.ui.View):
    def __init__(self, embeds, author, timeout=60):
        super().__init__(timeout=timeout)
        self.embeds = embeds
        self.author = author  # Store the author
        self.current_page = 0
        self.update_buttons()
        self.message = None  # Initialize message attribute

    def update_buttons(self):
        self.previous_button.disabled = self.current_page == 0
        self.next_button.disabled = self.current_page == len(self.embeds) - 1

    async def on_timeout(self):
        if self.message:
            for child in self.children:
                if isinstance(child, discord.ui.Button):
                    child.disabled = True
            try:
                await self.message.edit(view=None)
            except discord.NotFound:
                pass

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user != self.author:
            return False
        return True

    @discord.ui.button(label="◀", style=discord.ButtonStyle.primary)
    async def previous_button(self, button, interaction):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_buttons()
            try:
                await interaction.response.edit_message(embed=self.embeds[self.current_page], view=self)
            except discord.NotFound:
                pass

    @discord.ui.button(label="▶", style=discord.ButtonStyle.primary)
    async def next_button(self, button, interaction):
        if self.current_page < len(self.embeds) - 1:
            self.current_page += 1
            self.update_buttons()
            try:
                await interaction.response.edit_message(embed=self.embeds[self.current_page], view=self)
            except discord.NotFound:
                pass
