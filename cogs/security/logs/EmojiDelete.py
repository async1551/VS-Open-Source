import discord
from discord.ext import commands
import datetime

class EmojiDelete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_emojis_update(self, guild, before, after):
        logs = self.bot.get_channel(1366135572673990759) #add your log's channel id here
        
        removed_emoji = [emoji for emoji in before if emoji not in after]

        if removed_emoji:
            removed_by = await self.get_audit_log_entry(guild, discord.AuditLogAction.emoji_delete)

            removedembed = discord.Embed(
                title="Someone removed an emoji from the server!",
                colour=discord.Color.red()
            )
            removedembed.add_field(
                name="<:User_ID:1366110932731695305>・Moderator:",
                value=f"{removed_by.mention if removed_by else 'Unknown User'} - `{removed_by.display_name if removed_by else '-'}` - `{removed_by.id if removed_by else '-'}`",
                inline=False
            )
            removedembed.add_field(
                name="<:emojiremove:1366138249814343731>・Deleted emoji:",
                value="\n".join(f"`<:{emoji.name}:{emoji.id}>`" for emoji in removed_emoji),
                inline=False
            )
            removedembed.add_field(
                name="<:timer:1366110922413969530>・Date:",
                value=f"<t:{int(datetime.datetime.now().timestamp())}:R>",
                inline=False
            )
            await logs.send(embed=removedembed)

    async def get_audit_log_entry(self, guild, action_type):
        async for entry in guild.audit_logs(limit=1, action=action_type):
            return entry.user
        return None 

async def setup(bot):
    await bot.add_cog(EmojiDelete(bot))

