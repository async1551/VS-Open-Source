import discord
from discord.ext import commands
import datetime
import json
import os


class EmojiCreate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_emojis_update(self, guild, before, after):
        logs = self.bot.get_channel(1366135572673990759) #add your log's channel id here 

        added_emoji = [emoji for emoji in after if emoji not in before]
        if added_emoji:
            added_by = await self.get_audit_log_entry(guild, discord.AuditLogAction.emoji_create)

            addedembed = discord.Embed(
                title="Someone added a new emoji to the server!",
                colour=discord.Color.from_rgb(8, 34, 62)
            )

            addedembed.add_field(
                name="<:User_ID:1366110932731695305>・Moderator:",
                value=f"{added_by.mention if added_by else 'Unknown User'} - `{added_by.display_name if added_by else '-'}` - `{added_by.id if added_by else '-'}`",
                inline=False
            )
            addedembed.add_field(
                name="<:emojiadd:1366138267539341322>・New emoji:",
                value="\n".join(f"{emoji} (`\\:{emoji.name}:`)" for emoji in added_emoji),
                inline=False
            )
            addedembed.add_field(
                name="<:timer:1366110922413969530>・Date:",
                value=f"<t:{int(datetime.datetime.now().timestamp())}:R>",
                inline=False
            )

            await logs.send(embed=addedembed)

    async def get_audit_log_entry(self, guild, action_type):
        async for entry in guild.audit_logs(limit=1, action=action_type):
            return entry.user
        return None 

async def setup(bot):
    await bot.add_cog(EmojiCreate(bot))

