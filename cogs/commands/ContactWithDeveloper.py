#you can change the colors and the emojis if you want to
import discord
from discord.ext import commands, tasks
from datetime import *

class ContactWithDeveloper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.developer_id = 1260190202870366238 # add your user ID here, so you can get the messages (for the dev)

        @self.bot.tree.command(name="contact-developer", description="Contact with the developer of the bot.")
        async def contact_developer(interaction: discord.Interaction, message: str):
            developer = self.bot.get_user(self.developer_id)
            embed = discord.Embed(
                title = "<a:Developing_ZilGif:1376976270029623376>・Someone contacted you via `/contact-developer` slash command",
                color = discord.Color.from_rgb(33, 158, 188)
            )
            embed.add_field(
                name="<a:addi_messages:1376978945857163315>・Message Content:",
                value=f"**__{message}__**"
            )
            embed.add_field(
                name="<a:members:1367177747050270771>・Message Author:",
                value=f"{interaction.user.name} - `{interaction.user.display_name}` - `{interaction.user.id}`"
            )
            embed.add_field(
                name="<:timer:1366110922413969530>・Timestamp:",
                value=f"<t:{int(datetime.now().timestamp())}:R>"
            )
            await developer.send(embed=embed)
            doneembed = discord.Embed(
                title=f"Your message was successfully sent to the developer!",
                description=f"> <a:z_arrow_blue:1366138434212855940> **__Your message was sent to the developer successfully! He will contact you as soon as possible so that he can resolve your issue or question ASAP.__**",
                color = discord.Color.from_rgb(33, 158, 188)
            )
            await interaction.response.send_message(ephemeral=True, embed=doneembed)


async def setup(bot):
    await bot.add_cog(ContactWithDeveloper(bot))
