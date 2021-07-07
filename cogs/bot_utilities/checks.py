import discord
from datetime import date
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

    @staticmethod
    def is_valid_date(month, day, year=date.today().year):
        """Function to check if a date is a valid date.

           This check will not decide if the user can use the command or not like the above checks,
           this will help us to know if a date argument is a valid date, i will use it in the $set-bday command for example.
        """
        if year <= date.today().year and year > 1:
            if month <= 12:
            
                if month in {1, 3, 5, 7, 8, 10, 12} and day <= 31:
                    return True
            
                elif month in {4, 6, 9, 11} and day <= 30:
                    return True

                elif month == 2 and day <= 28:
                    return True

                else:
                    return False

            else:
                return False
        else:
            return False

