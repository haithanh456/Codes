cat > extra/Codes/Codes/__init__.py << 'EOF'
async def setup(bot):
    from .cog import CodesCog
    await bot.add_cog(CodesCog(bot))
EOF
