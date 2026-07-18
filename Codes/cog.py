import discord
from discord import app_commands
from discord.ext import commands
from django.utils import timezone

class CodesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="code", description="Redeem a code")
    @app_commands.describe(code="Enter the redeem code")
    async def code(self, interaction: discord.Interaction, code: str):
        from bd_models.models import Player, BallInstance
        from Codes.models import RedeemCode

        code = code.strip().upper()

        try:
            redeem = await RedeemCode.objects.select_related("ball", "special").aget(code__iexact=code)
        except RedeemCode.DoesNotExist:
            await interaction.response.send_message("code doesnt exist", ephemeral=True)
            return

        if not redeem.is_active:
            await interaction.response.send_message("code doesnt exist anymore", ephemeral=True)
            return

        if redeem.expires_at and redeem.expires_at < timezone.now():
            await interaction.response.send_message("code doesnt exist anymore", ephemeral=True)
            return

        if redeem.current_uses >= redeem.max_uses:
            await interaction.response.send_message("code doesnt exist anymore", ephemeral=True)
            return

        player, _ = await Player.objects.aget_or_create(discord_id=interaction.user.id)

        if redeem.ball:
            await BallInstance.objects.acreate(
                player=player,
                ball=redeem.ball,
                special=redeem.special,
                tradeable=True,
            )
            ball_name = redeem.ball.country
            if redeem.special:
                ball_name = f"{redeem.special.name} {ball_name}"
            message = f"You just claimed {ball_name}"
        else:
            message = "You just claimed the reward!"

        redeem.current_uses += 1
        await redeem.asave()

        await interaction.response.send_message(message, ephemeral=True)

async def setup(bot):
    await bot.add_cog(CodesCog(bot))
