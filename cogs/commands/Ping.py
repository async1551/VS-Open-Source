import discord
from discord.ext import commands
import time
import platform
import psutil
from datetime import timedelta, datetime


class PingCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.start_time = datetime.now()

        @self.bot.tree.command(name="ping", description="Show bot latency and advanced information.")
        async def ping(interaction: discord.Interaction):
            start_time = time.time()
            await interaction.response.send_message("Pinging...")
            end_time = time.time()

            latency = round(self.bot.latency * 1000, 2)
            response_time = round((end_time - start_time) * 1000, 1)
            ram_usage = psutil.Process().memory_info().rss / 1024 ** 2
            uptime = timedelta(seconds=(datetime.now() - self.start_time).total_seconds())
            status = self.bot.status
            shard_info = f"{interaction.guild.shard_id + 1}/{self.bot.shard_count}" if self.bot.shard_count else "No Sharding"
            uptime_seconds = int((datetime.now() - self.start_time).total_seconds())
            formatted_uptime = str(timedelta(seconds=uptime_seconds))

            embed = discord.Embed(title="Vibe City", color=discord.Color.blurple())
            embed.add_field(name="Ping", value=f"{latency}", inline=True)
            embed.add_field(name="RAM Usage", value=f"{ram_usage:.2f} MB", inline=True)
            embed.add_field(name="Uptime", value=f"{formatted_uptime}", inline=True)
            embed.add_field(name="Shards", value=shard_info, inline=True)
            embed.add_field(name="Bot Status", value=str(status), inline=True)
            embed.set_footer(text=f"dsc.gg/vicecityn1 | Join Now!", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
            embed.set_thumbnail(url=self.bot.user.avatar.url if self.bot.user.avatar else None)

            await interaction.edit_original_response(content=None, embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(PingCog(bot))

