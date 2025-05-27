import discord
from discord.ext import commands
import datetime

class EmojiUpdate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_emojis_update(self, guild, before, after):
        logs = self.bot.get_channel(1366135572673990759) #add your log's channel id here
        updated_emoji = [(b, a) for b in before for a in after if b.id == a.id and b.name != a.name]
        if updated_emoji:
            updated_by = await self.get_audit_log_entry(guild, discord.AuditLogAction.emoji_update)
            updatedembed = discord.Embed(title="A user renamed an emoji", colour=discord.Color.orange())
            updatedembed.add_field(
                name="<:User_ID:1366110932731695305>・Moderator:",
                value=f"{updated_by.mention if updated_by else 'Unknown'}",
                inline=False)
            updatedembed.add_field(
                name="<:emojiupdate:1366138223633498133>・Updated emoji:",
                value="\n".join(f"{b} (`\\:{b.name}:`) <a:right_arrow:1348091470103445644> {a} (`\\:{a.name}:`)" for b, a in updated_emoji),
                inline=False
            )
            updatedembed.add_field(
                name="<:timer:1366110922413969530>・Date:",
                value=f"<t:{int(datetime.datetime.now().timestamp())}:R>",
                inline=False)
            await logs.send(embed=updatedembed)

    async def get_audit_log_entry(self, guild, action_type):
        async for entry in guild.audit_logs(limit=1, action=action_type):
            return entry.user
        return None 

async def setup(bot):
    await bot.add_cog(EmojiUpdate(bot))
