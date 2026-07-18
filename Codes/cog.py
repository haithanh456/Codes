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
            message = f"✅ Success! You received **{ball_name}**{rarity_text}!"

        elif redeem.reward_type == "currency":
            if hasattr(player, "credits"):
                player.credits += redeem.currency_amount
                await player.asave()
                message = f"✅ Success! You received **{redeem.currency_amount} coins**!"
            else:
                message = f"✅ Success! You received **{redeem.currency_amount} coins**!"
        else:
            message = "❌ Code doesn't exist."

        redeem.current_uses += 1
        await redeem.asave()
        await interaction.followup.send(message, ephemeral=True)


class CodesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="codes", description="Redeem a code")
    async def codes(self, interaction: discord.Interaction):
        await interaction.response.send_modal(CodeModal())

    @app_commands.command(name="sync", description="Force sync commands")
    async def sync(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        try:
            synced = await self.bot.tree.sync()
            await interaction.followup.send(f"✅ Synced {len(synced)} commands! Try /codes now.", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"❌ Sync failed: {e}", ephemeral=True)


async def setup(bot):
    cog = CodesCog(bot)
    await bot.add_cog(cog)
    print("✅ Codes Cog loaded successfully!")
