import discord
from discord import app_commands
from discord.ext import commands
from django.utils import timezone

class CodeModal(discord.ui.Modal, title="Enter Code"):
    code_input = discord.ui.TextInput(
        label="Code",
        placeholder="Type the code here...",
        required=True,
        max_length=50
    )

    async def on_submit(self, interaction: discord.Interaction):
        from bd_models.models import Player, BallInstance
        from Codes.models import RedeemCode

        await interaction.response.defer(ephemeral=True)
        code = self.code_input.value.strip().upper()

        try:
            redeem = await RedeemCode.objects.select_related("ball", "special").aget(code__iexact=code)
        except RedeemCode.DoesNotExist:
            await interaction.followup.send("❌ This code is invalid!", ephemeral=True)
            return
        except Exception:
            await interaction.followup.send("❌ Something went wrong.", ephemeral=True)
            return

        if not redeem.is_active or (redeem.expires_at and redeem.expires_at < timezone.now()):
            await interaction.followup.send("❌ This code has expired!", ephemeral=True)
            return

        if redeem.max_uses > 0 and redeem.current_uses >= redeem.max_uses:
            await interaction.followup.send("❌ This code has reached its maximum uses!", ephemeral=True)
            return

        player, _ = await Player.objects.aget_or_create(discord_id=interaction.user.id)

        if redeem.ball:
            await BallInstance.objects.acreate(
                player=player,
                ball=redeem.ball,
                special=redeem.special,
                tradeable=True,
            )
            ball_name = getattr(redeem.ball, 'country', str(redeem.ball))
            if redeem.special:
                ball_name = f"{redeem.special.name} {ball_name}"
            message = f"✅ You have claimed **{ball_name}**!"
        else:
            message = f"✅ Code redeemed successfully!"

        redeem.current_uses += 1
        await redeem.asave()

        await interaction.followup.send(message, ephemeral=True)


class CodesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="codes", description="Redeem a code")
    async def codes(self, interaction: discord.Interaction):
        try:
            await interaction.response.send_modal(CodeModal())
        except discord.errors.NotFound:
            pass


async def setup(bot):
    await bot.add_cog(CodesCog(bot))
