import discord
from discord import app_commands
from discord.ext import commands
from django.utils import timezone

class CodesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="code", description="Redeem a code")
    @app_commands.describe(code="Enter your redeem code here")
    async def code(self, interaction: discord.Interaction, code: str):
        from bd_models.models import Player, BallInstance
        from Codes.models import RedeemCode

        # Defer immediately to prevent "Unknown interaction"
        await interaction.response.defer(ephemeral=True)

        code = code.strip().upper()

        try:
            redeem = await RedeemCode.objects.aget(code__iexact=code)
        except Exception:
            await interaction.followup.send("❌ Code doesn't exist.", ephemeral=True)
            return

        if not redeem.is_active or (redeem.expires_at and redeem.expires_at < timezone.now()):
            await interaction.followup.send("❌ Code doesn't exist.", ephemeral=True)
            return

        if redeem.current_uses >= redeem.max_uses:
            await interaction.followup.send("❌ This code has reached its maximum uses.", ephemeral=True)
            return

        player, _ = await Player.objects.aget_or_create(discord_id=interaction.user.id)

        if redeem.reward_type in ["ball", "ball_special"]:
            if not redeem.ball:
                await interaction.followup.send("❌ Code doesn't exist.", ephemeral=True)
                return

            await BallInstance.objects.acreate(
                player=player,
                ball=redeem.ball,
                special=redeem.special,
                tradeable=True,
            )

            ball_name = redeem.ball
            if redeem.special:
                ball_name = f"{redeem.special} {ball_name}"
            
            rarity_text = f" ({redeem.rarity})" if hasattr(redeem, 'rarity') and redeem.rarity else ""
            message = f"✅ You claimed: **{ball_name}**{rarity_text}!"

        elif redeem.reward_type == "currency":
            if hasattr(player, "credits"):
                player.credits += redeem.currency_amount
                await player.asave()
                message = f"✅ You claimed: **{redeem.currency_amount} coins**!"
            else:
                message = f"✅ You claimed: **{redeem.currency_amount} coins**!"
        else:
            message = "❌ Code doesn't exist."

        redeem.current_uses += 1
        await redeem.asave()

        await interaction.followup.send(message, ephemeral=True)


async def setup(bot):
    await bot.add_cog(CodesCog(bot))
    print("✅ Codes package loaded successfully!")
