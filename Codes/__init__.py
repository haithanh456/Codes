from .cog import CodesCog

async def setup(bot):
    await bot.add_cog(CodesCog(bot))
