import discord
from discord.ext import commands
from discord.utils import get
import asyncio

import re 


class ModerationCog(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot


    @commands.command(name = "kick",
                    usage="<@user/ID>",
                    description = "Kick a user.")
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def kick(self, ctx:commands.Context, member, *reason):

        # Get the user
        member = re.findall(r'\d+', member) 
        guild = ctx.guild
        memberToKick = get(guild.members, id=int(member[0]))

        if memberToKick:
            try:
                reason = " ".join(reason)
                embed = discord.Embed(title = self.bot.translate.msg(ctx.guild.id, "moderation", "YOU_HAVE_BEEN_KICKED").format(guild.name), description = self.bot.translate.msg(ctx.guild.id, "moderation", "KICK_REASON").format(reason), color = 0xff0000)
                await memberToKick.send(embed = embed)
                
                await memberToKick.kick()
                
                if reason:
                    await ctx.channel.send(self.bot.translate.msg(ctx.guild.id, "moderation", "HAS_BEEN_KICKED_WHITH_REASON").format(memberToKick, reason))
                else:
                    await ctx.channel.send(self.bot.translate.msg(ctx.guild.id, "moderation", "HAS_BEEN_KICKED_WHITHOUT_REASON").format(memberToKick))
            
            except Exception as error:
                return await ctx.channel.send(self.bot.translate.msg(ctx.guild.id, "global", "ERROR_OCCURED").format(error))

        else:
            await ctx.channel.send(self.bot.translate.msg(ctx.guild.id, "moderation", "MEMBER_NOT_FOUND"))
    

    @commands.command(name = "ban",
                    usage="<@user/ID>",
                    description = "Ban a user.")
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def ban(self, ctx:commands.Context, member, **reason):

        # Get the user
        member = re.findall(r'\d+', member) 
        guild = ctx.guild
        memberToBan = get(guild.members, id=int(member[0]))

        if memberToBan:
            try:
                reason = " ".join(reason)
                embed = discord.Embed(title = self.bot.translate.msg(ctx.guild.id, "moderation", "YOU_HAVE_BEEN_BANNED"), description = self.bot.translate.msg(ctx.guild.id, "moderation", "BAN_REASON").format(reason), color = 0xff0000)
                await memberToBan.send(embed = embed)
                
                await memberToBan.ban()

                if reason:
                    await ctx.channel.send(self.bot.translate.msg(ctx.guild.id, "moderation", "HAS_BEEN_BANNED_WHITH_REASON").format(memberToBan, reason))
                else:
                    await ctx.channel.send(self.bot.translate.msg(ctx.guild.id, "moderation", "HAS_BEEN_BANNED_WHITHOUT_REASON").format(memberToBan))
            
            except Exception as error:
                return await ctx.channel.send(self.bot.translate.msg(ctx.guild.id, "global", "ERROR_OCCURED").format(error))
            
        else:
            await ctx.channel.send(self.bot.translate.msg(ctx.guild.id, "moderation", "MEMBER_NOT_FOUND"))

# Clear command
    
    @commands.command(name='clear', aliases=['remove','purge'])
    async def clear(self, ctx, amount: int):
        if ctx.message.author.guild_permissions.manage_messages:
            try:
                if amount > 0 and amount < 300:
                    await ctx.channel.purge(limit=amount + 1)
                    await asyncio.sleep(0.5)
                    msg = await ctx.send(f"Removed {amount} messages!")
                    await asyncio.sleep(1.5)
                    await msg.delete()
                else:
                    await ctx.send(f'{ctx.message.author.mention}, Enter an amount between 0 and 30, cannot delete {amount} messages!')
            except Exception as e:
                await ctx.send(e)
        else:
            embed = discord.Embed(
                        title='**YOU ARE NOT AUTHORIZED**',
                        description="You do not have the authorization to perform this action\nYour action will be reported",
                        colour=0xff0000
                )
            await ctx.send(embed=embed)
            channel = discord.utils.get(ctx.guild.channels, name='moderation-logs')
            if channel is not None:
                emb = discord.Embed(title='Illegal use of command **clear**', description=f'{ctx.author.mention} Used the `clear` command, Who is not authorized', colour=0xff0000)
                await channel.send(embed=emb)


    # Clear command: Error handling
    
    @clear.error
    async def clear_error(self, ctx, error):
        
        if isinstance(error, commands.MissingRequiredArgument):
            if ctx.message.author.guild_permissions.manage_messages:
                await ctx.send(f'How many do you want to remove, {ctx.author.mention}?')
            else:
                embed = discord.Embed(
                        title='**YOU ARE NOT AUTHORIZED**',
                        description="You do not have the authorization to perform this action\nYour action will be reported",
                        colour=0xff0000
                )
                await ctx.send(embed=embed)
                channel = None
                if (int(ctx.guild.id)) is not None:
                    channel = self.bot.get_channel(int(ctx.guild.id)["channel_id"])
                if channel is not None:
                    emb = discord.Embed(title='Illegal use of command **clear**', description=f'{ctx.author.mention} Used the `clear` command, Who is not authorized', colour=0xff0000)
                    await channel.send(embed=emb)
        elif isinstance(error, commands.BadArgument):
            await ctx.send(f'Please enter a valid amount {ctx.message.author.mention}')
        elif isinstance(error, discord.Forbidden):
            await ctx.send('I do not have enough permissions!')
        else:
            await ctx.send(f'An error occured \n```\n{error}\n```\nPlease check the console for traceback, or raise an issue to CABREX')
            raise error

def setup(bot:commands.Bot):
    bot.add_cog(ModerationCog(bot))