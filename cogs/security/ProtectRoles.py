import discord
from discord.ext import commands
import json
import os
from datetime import datetime
import pytz

config_path = os.path.join(os.path.dirname(__file__), "config.json")
with open(config_path, "r") as file:
    config = json.load(file)

PROTECTED_ROLES = set(config["protected_roles"])
ALLOWED_ROLES = set(config["allowed_roles"])
LOG_CHANNEL_ID = config["log_channel"]

class ProtectRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.roles == after.roles:
            return

        for role in after.roles:
            if role.id in PROTECTED_ROLES and role not in before.roles:
                async for entry in after.guild.audit_logs(limit=1, action=discord.AuditLogAction.member_role_update):
                    if entry.target == after and role in entry.after.roles and not any(r.id in ALLOWED_ROLES for r in entry.user.roles):
                        await after.remove_roles(role)
                        await self.log_violation(entry, after, role)

    async def log_violation(self, entry, member, role):
        log_channel = self.bot.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            embed = discord.Embed(title="Unauthorized Role Addition", color=discord.Color.dark_red())
            embed.add_field(name="Moderator", value=f"{entry.user.mention} ({entry.user.id})", inline=False)
            embed.add_field(name="Role", value=f"{role.mention} ({role.id})", inline=False)
            embed.add_field(name="User", value=f"{member.mention} ({member.id})", inline=False)
            embed.add_field(name="Time", value=f"<t:{int(datetime.now(pytz.timezone('Europe/Athens')).timestamp())}:R>", inline=False)
            await log_channel.send(embed=embed, view=RoleActionButtons(member, role))

class RoleActionButtons(discord.ui.View):
    def __init__(self, member="", role=""):
        super().__init__(timeout=None)
        self.member = member
        self.role = role

    @discord.ui.button(label="Restore Role", style=discord.ButtonStyle.gray, custom_id="restorerolebuttoncustomid")
    async def restore_role(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.member.add_roles(self.role)
        await interaction.response.send_message(f"✅ Restored role **{self.role.name}** for **{self.member.name}**.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ProtectRoles(bot))
    bot.add_view(RoleActionButtons())
