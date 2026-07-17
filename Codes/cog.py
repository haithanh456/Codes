import discord
from discord import app_commands
from discord.ext import commands
from django.utils import timezone

class CodesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="code", description="Redeem a code")
    @app_commands.describe(code="The redeem code")
    async def code(self, interaction: discord.Interaction, code: str):
        from bd_models.models import Player, BallInstance
        from Codes.models import RedeemCode

        code = code.strip().upper()

        try:
            redeem = await RedeemCode.objects.aget(code__iexact=code)
        except RedeemCode.DoesNotExist:
            await interaction.response.send_message("❌ This code is invalid!", ephemeral=True)
            return
        except Exception:
            await interaction.response.send_message("❌ Something went wrong.", ephemeral=True)
            return

        if not redeem.is_active or (redeem.expires_at and redeem.expires_at < timezone.now()):
            await interaction.response.send_message("❌ This code has expired!", ephemeral=True)
            return

        if redeem.max_uses > 0 and redeem.current_uses >= redeem.max_uses:
            await interaction.response.send_message("❌ This code has reached its maximum uses!", ephemeral=True)
            return

        player, _ = await Player.objects.aget_or_create(discord_id=interaction.user.id)

        if redeem.ball:
            await BallInstance.objects.acreate(
                player=player,
                ball=redeem.ball,
                special=redeem.special,
                tradeable=True,
            )
            ball_name = redeem.ball.country if hasattr(redeem.ball, 'country') else str(redeem.ball)
            if redeem.special:
                ball_name = f"{redeem.special.name} {ball_name}"
            message = f"✅ You have claimed **{ball_name}** using code `{code}`!"
        else:
            message = f"✅ Code `{code}` redeemed successfully!"

        redeem.current_uses += 1
        await redeem.asave()

        await interaction.response.send_message(message, ephemeral=True)


async def setup(bot):
    await bot.add_cog(CodesCog(bot))
