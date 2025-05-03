
import discord
from discord.ext import commands
import asyncio
from datetime import *
import aiohttp


class ChangeNameModal(discord.ui.Modal, title="Change bot's name"):
    new_name = discord.ui.TextInput(label="New Name", placeholder="Vice City", custom_id="changenamemodalcustomid")
    
    async def on_submit(self, interaction: discord.Interaction):
        try:
            embed = discord.Embed(description="<a:sync_incircle:1366820466207101009>・Changing bot's name...", colour=0x5acfa6)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            await asyncio.sleep(5)
            await interaction.client.user.edit(username=self.new_name.value)
            doneembed = discord.Embed(description="<a:thehell_check:1366143045967286362>・Successfully changed bot's name", colour=0x5acfa6)
            await interaction.edit_original_response(embed=doneembed)
            logsembed = discord.Embed(
                title="Someone changed bot's name via control panel",
                colour=discord.Colour.green())
            logsembed.add_field(
                name="<:trainee_mod:1366110937156947999>・Responsible Moderator",
                value=f"{interaction.user.mention} - `{interaction.user.display_name}` - `{interaction.user.id}`",
                inline=False
            )
            logsembed.add_field(
                name="<:User_ID:1366110932731695305>・New Name:",
                value=f"{self.new_name.value}",
                inline=False
            )
            logsembed.add_field(
                    name="**<:timer:1366110922413969530>・Date:**",
                    value=f"<t:{int(datetime.now().timestamp())}:R>",
                    inline=False,
            )
            await interaction.guild.get_channel(1366820028132888597).send(embed=logsembed)
        except discord.HTTPException as e:
            await interaction.response.send_message(f"Error : {e}", ephemeral=True)


class ChangeIconModal(discord.ui.Modal, title="Change bot's icon url"):
    url = discord.ui.TextInput(label="Icon URL", placeholder="Please submit the url of the new icon", custom_id="changeiconmodalcustomid")
    
    async def on_submit(self, interaction: discord.Interaction):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url.value) as response:
                if response.status == 200:
                    data = await response.read()
                    try:
                        embed = discord.Embed(description="<a:sync_incircle:1366820466207101009>・Change the avatar of the bot....", colour=0x5acfa6)
                        await interaction.response.send_message(embed=embed, ephemeral=True)
                        await asyncio.sleep(3)
                        await interaction.client.user.edit(avatar=data)
                        doneembed = discord.Embed(description="<a:thehell_check:1366143045967286362>・Successful change of the bot avatar", colour=0x5acfa6)
                        await interaction.edit_original_response(embed=doneembed)
                        log_channel = interaction.guild.get_channel(1366820028132888597)
                        if log_channel:
                            log_embed = discord.Embed(
                                title=f"<a:dev:1366841852342435840>・A user changed the avatar of the bot via the configuration panel.",
                                colour=discord.Colour.green()
                            )
                            log_embed.add_field(
                                name="<:trainee_mod:1366110937156947999>・Moderator",
                                value=f"{interaction.user.mention} - `{interaction.user.display_name}` - `{interaction.user.id}`",
                                inline=False
                            )
                            log_embed.add_field(
                                name="<a:Url_Gif1:1366841677561462905>・URL:",
                                value=f"{self.url.value}",
                                inline=False
                            )
                            log_embed.add_field(
                                name="<:timer:1366110922413969530>・Date",
                                value=f"<t:{int(datetime.now().timestamp())}:R>",
                                inline=False
                            )
                            await log_channel.send(embed=log_embed)
                    except discord.HTTPException as e:
                        await interaction.response.send_message(f"Failure detected while changing bot's icon: {e}", ephemeral=True)
                else:
                    await interaction.response.send_message("Failed to capture the image. Make sure the URL is correct.", ephemeral=True)


class ChangeStatusModal(discord.ui.Modal, title="Change the status of the bot"):
    status = discord.ui.TextInput(label="Enter the new status.", placeholder="(online, idle, dnd, invisible)", custom_id="changestatuscustomid")
    
    async def on_submit(self, interaction: discord.Interaction):
        status_dict = {
            'online': discord.Status.online,
            'idle': discord.Status.idle,
            'dnd': discord.Status.do_not_disturb,
            'offline': discord.Status.invisible
        }
        if self.status.value.lower() in status_dict:
            embed = discord.Embed(description="<a:sync_incircle:1366820466207101009>・Change the status of the bot...", colour=0x5acfa6)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            await asyncio.sleep(4)
            await interaction.client.change_presence(status=status_dict[self.status.value.lower()])
            doneembed = discord.Embed(description="<a:thehell_check:1366143045967286362>・Successful change of bot status", colour=0x5acfa6)
            await interaction.edit_original_response(embed=doneembed)
            log_channel = interaction.guild.get_channel(1366820028132888597)
            log_embed = discord.Embed(
                title=f"<a:pink_status:1366843176266104903>・A user changed the status of the bot via the configuration panel.",
                colour=discord.Colour.green()
            )
            log_embed.add_field(
                name="<:trainee_mod:1366110937156947999>・Moderator",
                value=f"{interaction.user.mention} - `{interaction.user.display_name}` - `{interaction.user.id}`",
                inline=False
            )
            log_embed.add_field(
                name="<a:pink_status:1366843176266104903>・New Status:",
                value=f"{self.status.value}",
                inline=False)
            log_embed.add_field(
                name="<:timer:1366110922413969530>・Date:",
                value=f"<t:{int(datetime.now().timestamp())}:R>",
                inline=False
            )
            await log_channel.send(embed=log_embed)
        else:
            await interaction.response.send_message("**Invalid activity type.** Valid options are: `online`, `idle`, `dnd`,.", ephemeral=True)
            

class ChangeActivityModal(discord.ui.Modal, title="Change Bot activity"):
    activity_type = discord.ui.TextInput(label="Enter the type of activity.", placeholder="(playing, listening, watching)", custom_id="changeactivitycustomid")
    activity_name = discord.ui.TextInput(label="Name of activity", placeholder="Type the name of the activity", custom_id="changeactivitynamecustomid")
    
    async def on_submit(self, interaction: discord.Interaction):
        activity_type_lower = self.activity_type.value.lower()
        activity_name = self.activity_name.value

        if activity_type_lower == "playing":
            activity = discord.Game(name=activity_name)
        elif activity_type_lower == "listening":
            activity = discord.Activity(type=discord.ActivityType.listening, name=activity_name)
        elif activity_type_lower == "watching":
            activity = discord.Activity(type=discord.ActivityType.watching, name=activity_name)
        else:
            await interaction.response.send_message("**Invalid activity type.** Valid options are: `playing`, `listening`, `watching`.", ephemeral=True)
            return

        embed = discord.Embed(description="<a:sync_incircle:1366820466207101009>・Change bot's activity", colour=0x5acfa6)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        await asyncio.sleep(5)

        await interaction.client.change_presence(activity=activity)

        doneembed = discord.Embed(description=f"<a:thehell_check:1366143045967286362>・Successfully changed the bot's activity to {activity_type_lower} {activity_name}", colour=0x5acfa6)
        await interaction.edit_original_response(embed=doneembed)
        log_channel = interaction.guild.get_channel(1366820028132888597)
        if log_channel:
            log_embed = discord.Embed(
                title=f"<a:active_player:1366843546409238668>・A user changed the activity of the bot via the configuration panel.",
                colour=discord.Colour.green()
            )
            log_embed.add_field(
                name="<:trainee_mod:1366110937156947999>・Moderator",
                value=f"{interaction.user.mention} - `{interaction.user.display_name}` - `{interaction.user.id}`",
                inline=False
            )
            log_embed.add_field(
                name="<a:active_player:1366843546409238668>・Activity Type:",
                value=f"{activity_type_lower}",
                inline=False
            )
            log_embed.add_field(
                name="<a:chat_active:1366843379895242922>・Activity:",
                value=f"{activity_name}",
                inline=False
            )
            log_embed.add_field(
                name="<:timer:1366110922413969530>・Date",
                value=f"<t:{int(datetime.now().timestamp())}:R>",
                inline=False
            )
            await log_channel.send(embed=log_embed)



class PanelView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button( 
        emoji="<a:sync_incircle:1366820466207101009>",
        label="・Sync",
        style=discord.ButtonStyle.gray,
        custom_id="panelviewsynccommandbuttoncustomid"
    )
    async def synccallback(self, interaction: discord.Interaction, button: discord.ui.Button):
        required_role_id = 1366821571888418917

        if not isinstance(interaction.user, discord.Member):
            await interaction.response.send_message("__**Could not verify your roles.**__", ephemeral=True)
            return

        if required_role_id not in [role.id for role in interaction.user.roles]:
            await interaction.response.send_message("__**You don't have permissions to sync commands.**__", ephemeral=True)
            return

        guild_id = 1281271317152399382
        guild = discord.Object(id=guild_id)
        synced = await self.bot.tree.sync(guild=guild)
        await interaction.response.send_message(f"✅ Synced {len(synced)} command(s) to the guild!", ephemeral=True)

    @discord.ui.button(
        emoji = "<:User_ID:1366110932731695305>",
        label = "・Change Name",
        style = discord.ButtonStyle.gray,
        custom_id = "panelviewchangenamebuttoncustomid"
    )
    async def changenamecallback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(ChangeNameModal())

    @discord.ui.button(
        emoji = "<a:Logo_Drip_Discord_Logo:1366840791179333732>",
        label = "・Change Icon",
        style = discord.ButtonStyle.gray,
        custom_id = "panelviewchangeiconbuttoncustomid"
    )
    async def changeiconcallback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(ChangeIconModal())

    @discord.ui.button(
        emoji = "<a:pink_status:1366843176266104903>",
        label = "・Change Status",
        style = discord.ButtonStyle.gray,
        custom_id = "panelviewchangestatusbuttoncustomid"
    )
    async def changestatuscallback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(ChangeStatusModal())

    @discord.ui.button(
        emoji = "<a:active_player:1366843546409238668>",
        label = "・Change Activity",
        style = discord.ButtonStyle.gray,
        custom_id = "panelviewchangeactivitybuttoncustomid"
    )
    async def changestatuscallback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(ChangeActivityModal())





class Panel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def panel(self, ctx):
        embed = discord.Embed(
            title="Bot Control Panel",
            colour = discord.Colour.teal()
        )
        embed.set_author(name="Vice City Policia", icon_url=ctx.guild.icon.url)
        await ctx.message.delete()
        await ctx.send(embed=embed, view=PanelView(bot=self.bot))

async def setup(bot):
    await bot.add_cog(Panel(bot))
    bot.add_view(PanelView(bot))
