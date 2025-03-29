import discord
from discord.ext import commands
import os

bot = commands.Bot(command_prefix=commands.when_mentioned_or('-'), intents=discord.Intents.all())


async def load_cogs():
    cog_directory = "./cogs"
    for root, dirs, files in os.walk(cog_directory):
        for file in files:
            if file.endswith(".py"):
                cog_name = os.path.splitext(os.path.relpath(os.path.join(root, file), cog_directory))[0]
                cog_name = cog_name.replace(os.sep, '.')
                try:
                    await bot.load_extension(f"cogs.{cog_name}")
                    print(f"Successfully loaded {cog_name}")
                except Exception as e:
                    print(f"Error loading cog {cog_name}: {e}")


@bot.event
async def on_ready():
  await load_cogs()
  print(f"Bot is ready and connected as: {bot.user}")


bot.run("YOUR BOT'S TOKEN GOES HERE")
