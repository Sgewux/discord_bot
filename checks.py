import discord
from discord.ext import commands


class CustomChecks(object):
    """CustomChecks is a class wich provide us with custom command checks as static methods.
    """

    @staticmethod
    async def is_bdays_channel(ctx):
        """ This function is a check to check if the user used the command in a channel named 'birthdays'.
        """
        if 'birthdays' in ctx.message.channel.name:
            return True
        else:
            raise commands.CommandError(message='You have to use this command in a channel named "birthdays" (with some emojis if you want 😉). Just to be tidy.')

    @staticmethod
    async def is_guild(ctx):
        """This function is a check to check if the user is using the command in a server.
        
            discord.py provide us with the guild_only() check. But i decided to use this custom one.
         """
        if ctx.guild:
            return True
        else:
            raise commands.CommandError(message='This command only works on servers.')
