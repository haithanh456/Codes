class CodesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="codes", description="Redeem a code")
    async def codes(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True, thinking=True)
        try:
            await interaction.followup.send_modal(CodeModal())
        except Exception:
            await interaction.followup.send("❌ Failed to open the modal.", ephemeral=True)
