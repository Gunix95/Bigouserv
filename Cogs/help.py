import discord
from discord.ext import commands
from Tools.utils import getGuildPrefix

# ------------------------ COGS ------------------------ #  

class HelpCog(commands.Cog, name="help command"):
    def __init__(self, bot):
        self.bot = bot

# ------------------------------------------------------ #  

    @commands.command(name = 'help',
                        usage="(commandName)",
                        description = "Display the help message.")
    @commands.cooldown(1, 3, commands.BucketType.member)
    async def help(self, ctx, commandName=None):

        commandName2 = None
        stop = False

        if commandName is not None:
            for i in self.bot.commands:
                if i.name == commandName.lower():
                    commandName2 = i
                    break 
                else:
                    for j in i.aliases:
                        if j == commandName.lower():
                            commandName2 = i
                            stop = True
                            break
                if stop:
                    break 

            if commandName2 is None:
                await ctx.channel.send("No command found!")   
            else:
                embed = discord.Embed(title=f"**{commandName2.name.upper()} COMMAND :**", color=0xdeaa0c)
                embed.set_thumbnail(url=f'{self.bot.user.avatar_url}')
                embed.add_field(name=f"**NAME :**", value=f"{commandName2.name}", inline=False)
                aliases = ""
                if len(commandName2.aliases) > 0:
                    for aliase in commandName2.aliases:
                        aliases = aliase
                else:
                    commandName2.aliases = None
                    aliases = None
                embed.add_field(name=f"**ALIASES :**", value=f"{aliases}", inline=False)
                if commandName2.usage is None:
                    commandName2.usage = ""
                    
                prefix = await getGuildPrefix(self.bot, ctx)
                embed.add_field(name=f"**USAGE :**", value=f"{prefix}{commandName2.name} {commandName2.usage}", inline=False)
                embed.add_field(name=f"**DESCRIPTION :**", value=f"{commandName2.description}", inline=False)
                await ctx.channel.send(embed=embed)
        else:
            prefix = await getGuildPrefix(self.bot, ctx)
            embed = discord.Embed(title=f"__**Help page of {self.bot.user.name.upper()}**__", description= "** *help (command) :**Display the help list or the help data for a specific command.", color=0xdeaa0c)
            embed.set_thumbnail(url=f'{self.bot.user.avatar_url}')
            embed.add_field(name=f"__ADMIN :__", value=f"**{prefix}setup <on/off> :** Active la protection par captcha.\n**{prefix}settings :** Detail tout les paramètre.**\n{prefix}giveroleaftercaptcha <role ID/off> :** Donne un rôle après avoir passer la verification.**\n{prefix}minaccountage <number (hours)> :** refuse les compté crée depuis un durée (24 hours by default).\n**{prefix}antinudity <true/false> :** Active ou desactive la protection de nudité.\n**{prefix}antiprofanity <true/false> :** Enable or disable the profanity protection.\n**{prefix}antispam <true/false> :** Active ou désactive la protection antispam.\n**{prefix}allowspam <#channel> (remove) :** Autorise ou refuse le spam dans un channel spécifique.\n**{prefix}lock | unlock <#channel/ID> :** Bigouverouille/déverouille le channel.\n\n**{prefix}kick <@user/ID> :** Kick un utilisateur.\n**{prefix}ban <@user/ID> :** ban un utilisateur.\n**{prefix}clear <nombre> :**Fait disparaitre un nombre de message**\n\n**{prefix}changeprefix <prefix> :** Change le prefix du bot.\n**{prefix}changelanguage <language> :** change la langue du Bigoubot.", inline=False)
            embed.add_field(name=f"__COMMANDS :__", value=f"**{prefix}userinfos <@user/ID> :** Get user infomations.\n**{prefix}ping :** Ca pong en fait...", inline=False)
            await ctx.channel.send(embed=embed)

# ------------------------ BOT ------------------------ #  

def setup(bot):
    bot.remove_command("help")
    bot.add_cog(HelpCog(bot))