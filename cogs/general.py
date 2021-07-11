import math
import json
import discord
from discord.ext import commands
from cogs.bot_utilities.checks import CustomChecks
from cogs.bot_utilities.weather_scraper import WeatherScraper


class GeneralCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self._bdays_data_path = './data/birth_days.json'
        self._members_data_path = './data/members_who_left.json'

    @commands.command(pass_context=True, aliases=('weather', 'WEATHER'))
    async def get_weather(self, ctx, *place):
        place = ''.join(place)
        await ctx.message.reply(content=f'Weather in {place} is currently: {WeatherScraper(place).get_temperature_and_weather()}')

    @commands.command(pass_context=True, aliases=('HMD', 'hmd'))
    async def time_belonging(self, ctx):
        if type(ctx.author) == discord.member.Member:
            join_date = ctx.author.joined_at
            current_date = datetime.datetime.now()
            delta = current_date - join_date
            await ctx.message.reply(content=f'You\'ve been on this server for {delta.days} days!')
        else:
            return None

    @commands.command(pass_context=True, aliases=('DTB', 'dtb'))
    async def decimal_to_binary(self, ctx, user_number: int):
        if user_number == 0:
            await ctx.message.reply(content=f'{user_number} in binary is 0')
            return 

        number = user_number
        residue = 0

        while ((math.log2(number)*10)%10) != 0: #While the log2 of number is not a whole number
            number -= 1
            residue += 1

        binary = ['0' for i in range(int(math.log2(number)) + 1)]
        binary[0] = '1'

        while residue > 0:
            subresidue = 0
            
            while ((math.log2(residue)*10)%10) != 0: #While the log2 of residue is not a whole number
                residue -= 1
                subresidue += 1

            binary[(int(math.log2(residue)) + 1) * -1] = '1'

            if subresidue > 0:
                residue = subresidue

            elif subresidue == 0:
                break

        await ctx.message.reply(content=f'{user_number} in binary is {"".join(binary)}')

    @commands.command(pass_context=True, aliases=('BTD', 'btd'))
    async def binary_to_decimal(self, ctx, user_number):

        user_number = user_number[::-1]
        decimal = 0
        for i in range(len(user_number)):
            if user_number[i] == '1':
                decimal += (2**i)

        await ctx.message.reply(content=f'{user_number} in decimal is {decimal}')

    @commands.command(pass_context=True, aliases=('set-bday', 'SET-BDAY'))
    @commands.check(CustomChecks.is_guild)
    @commands.check(CustomChecks.is_bdays_channel)
    async def set_bday(self, ctx, month: int, day: int):

        guild_id = str(ctx.guild.id)
        user_id = str(ctx.author.id)

        with open(self._bdays_data_path, 'r') as f:
            bdays_dict = json.load(f)

        try:
            server_bdays = bdays_dict[guild_id]

            if CustomChecks.is_valid_date(month, day):
                server_bdays[user_id] = (month, day)
            
            else:
                await ctx.message.reply(content="Please enter a valid date.")
                return None

        except KeyError:
            bdays_dict[guild_id] = {}
            server_bdays = bdays_dict[guild_id]

            if CustomChecks.is_valid_date(month, day):
                server_bdays[user_id] = (month, day)

            else:
                await ctx.message.reply(content="Please enter a valid date.")
                return None

        with open(self._bdays_data_path, 'w') as f:
            json.dump(bdays_dict, f)

        await ctx.message.reply(content="Birhtday saved 😉.")


    @set_bday.error
    async def set_bday_error_handler(self, ctx, error):
        """This function is for handling the errors wich be raised if the $set-bday command is not used properly.
        """
        if type(error) == commands.errors.CommandError:
            await ctx.message.reply(content= str(error))


        

