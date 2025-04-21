import discord
from discord.ext import commands
from datetime import *
import asyncio


class CloseTicket(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(
        label="・Close Ticket",
        custom_id="closeticketviewbutton",
        style = discord.ButtonStyle.danger
    )
    async def closeticket(self, button: discord.ui.Button, interaction: discord.Interaction):
        logschannel = button.guild.get_channel(1358475528100905211) # ADD YOUR LOGS CHANNEL ID HERE
        ticketownerid = button.channel.topic
        ticketowner = button.guild.get_member(int(ticketownerid)) if ticketownerid else None
        logsembed = discord.Embed(
            title="Ticket Closed",
            colour=discord.Colour.red()
        )
        logsembed.add_field(
            name="Ticket Closed",
            value=f"{button.channel.name}"
        )
        createddate = button.channel.created_at if button.channel else None
        logsembed.add_field(
            name="Created by",
            value=f"{ticketowner}・`{ticketowner.id}`" if ticketowner else "Unknown"
        )
        logsembed.add_field(
            name="Created Date",
            value=f"<t:{int(createddate.timestamp())}:F>" if createddate else "Unknown"
        )
        logsembed.add_field(
            name="Closed by",
            value=f"{button.user.mention}・`{button.user.id}`"
        )
        logsembed.add_field(
            name="Closed Date",
            value=f"<t:{int(button.created_at.timestamp())}:F>"
        )
        logsembed.set_author(
            name=button.guild.name,
            icon_url=button.guild.icon.url if button.guild.icon.url else None
        )
        embed = discord.Embed(
            description="This ticket closes in 5 seconds",
            colour=discord.Colour.dark_red()
        )
        countdownmessage = await button.channel.send(embed=embed)
        for i in range(4, 0, -1):
            await asyncio.sleep(1)
            embed2 = discord.Embed(
                description=f"This ticket closes in {i} seconds",
                colour=discord.Colour.dark_red()
            )
            await countdownmessage.edit(embed=embed2)
        await logschannel.send(embed=logsembed)
        await button.channel.delete()

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="・Open Ticket",
        custom_id="openticketviewbutton",
        style = discord.ButtonStyle.gray
    )
    async def buttonpress(self, button: discord.ui.Button, interaction: discord.Interaction):
        staffrole = button.guild.get_role(1353463688471908432) # ADD YOUR STAFF ROLE ID HERE
        ticketcategory = button.guild.get_channel(1358475281815568485) # ADD YOUR TICKETS CATEGORY ID HERE
        logschannel = button.guild.get_channel(1358475528100905211) # ADD YOUR LOGS CHANNEL ID HERE
        overwrites = {
            button.guild.default_role: discord.PermissionOverwrite(view_channel=False, read_messages=False),
            button.user: discord.PermissionOverwrite(view_channel=True, read_messages=True, send_messages=True),
            staffrole: discord.PermissionOverwrite(view_channel=True, read_messages=True, send_messages=True)
        }
        ticketchannel = await button.guild.create_text_channel(
            name=f"support-{button.user.name}",
            category=ticketcategory,
            overwrites=overwrites,
            topic=str(button.user.id)
        )
        logsembed = discord.Embed(
            title="Ticket Created",
            colour = discord.Colour.green()
        )
        logsembed.add_field(
            name="Ticket Name:",
            value=f"[{ticketchannel}](https://discord.com/channels/{button.guild.id}/{ticketchannel.id})"
        )
        logsembed.add_field(
            name="Created by:",
            value=f"{button.user.mention}・`{button.user.id}`"
        )
        logsembed.add_field(
            name="Opened Date",
            value=f"<t:{int(datetime.now().timestamp())}:F>"
        )
        logsembed.set_footer(text=f"Channel ID: {ticketchannel.id}")
        logsembed.set_author(name=f"{button.guild.name}", icon_url=button.guild.icon.url if button.guild.icon.url else None)
        await logschannel.send(embed=logsembed)
        ticketembed = discord.Embed(
            description=f"Good evening {button.user.mention}, a member of our team will be in contact with you shortly.\n\nIf you would like to close this ticket, click the button below!",
            colour=discord.Colour.og_blurple()
        )
        await ticketchannel.send(embed=ticketembed, view=CloseTicket())
        ticketcreatedembed = discord.Embed(
            description=f"Your ticket has been successfully created: {ticketchannel.mention}・`{ticketchannel.id}`",
            colour=discord.Colour.teal()
        )
        await button.response.send_message(embed=ticketcreatedembed, ephemeral=True)

        

class TicketSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ticket_setup(self, ctx):
        embed = discord.Embed(
            description=f"To create a ticket press the **・Open Ticket** button.",
            colour = discord.Colour.og_blurple()
        )
        embed.set_author(name=ctx.guild.name, icon_url = ctx.guild.icon.url if ctx.guild.icon.url else None)
        embed.set_thumbnail(url = ctx.guild.icon.url if ctx.guild.icon.url else None)
        await ctx.send(embed=embed, view=TicketView())
        await ctx.message.delete()


async def setup(bot: commands.Bot):
    await bot.add_cog(TicketSystem(bot))
    bot.add_view(CloseTicket())
    bot.add_view(TicketView())
