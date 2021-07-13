import math
import copy
import json
import discord
import datetime
from discord.ext import commands
from cogs.bot_utilities.checks import CustomChecks
from cogs.bot_utilities.weather_scraper import WeatherScraper


class GeneralCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self._bdays_data_path = './data/birth_days.json'
        self._members_data_path = './data/members_who_left.json'

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = self.bot.get_guild(member.guild.id)
        user_id = member.id
        user_mention = member.mention
        welcomes_channel = None
        for channel in guild.text_channels:
            if 'welcome' in channel.name:
                welcomes_channel = channel

        if welcomes_channel:
            with open(self._members_data_path, 'r') as f:
                members_who_left = json.load(f)
            
            server_data = members_who_left.get(str(guild.id), None)

            if server_data:
                if user_id in server_data:
                    await welcomes_channel.send(f'Welcome back {user_mention}! I hope you won\'t be planning to leave the server this time 🤨.')
                else:
                    await welcomes_channel.send(f'Welcome to this server {user_mention}! I hope you have a good time here 😄.')
            else:
                await welcomes_channel.send(f'Welcome to this server {user_mention}! I hope you have a good time here 😄.')


    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild = self.bot.get_guild(member.guild.id)
        user_id = member.id

        with open(self._members_data_path, 'r') as f:
            members_who_left = json.load(f)

        server_data = members_who_left.get(str(guild.id), None)

        if not server_data:
            server_data = [user_id]
        else:
            if user_id not in server_data:
                server_data.append(user_id)
        
        members_who_left[str(guild.id)] = server_data

        with open(self._members_data_path, 'w') as f:
            json.dump(members_who_left, f)


    @commands.command(pass_context=True)
    async def help(self, ctx):
        message_to_be_sent = """
        Hi 👋, my name is Diego Norrea 
        I'm a Discord bot 🤖 and i have the following commands:

        **General commands 🌎:**
        **-weather:** Given a place i will tell you the weather and temperature of that place.
        **-HMD:** To know how many days you have been on this server.
        **-sayto:** Given a quoted message and a user name i will send that message to that user throug dm chat. For example ("Hi, how is it going?" juanca galindo). I will delete your message imediatly and send the dm to the target user.
        **-set-bday:** To set your birthday use month day syntax using blank spaces to split values. For example ("06 23")
        **-next-bdays:** I will show the upcoming server's birthdays (today, next 7 days, current month).

        **Space commands 🚀:**
        **-APOD:** I will send the Astronomy Picture Of the Day.
        **-MRP:** I will send a random picture taken by the Curiosity mars rover.
        **-MRPD:** I will send a photo taken by the Curiosity mars rover in date with the year month day format given by you (use blank spaces to split the values).

        **Crypto commands 💱:**
            **-cprice:** Given a cryptocurrency name (bitcoin for example) and a normal currency (usd for example) i will send you the current price of that currency.
            **-CTC:** Given a normal currency name, cryptocurrency name and an amount i will Convert To Crypto that amount.
            **-CFC:** Given a cryptocurrency name, normal currency name and an amount i will Convert From Crypto that amount. Use the full name to reffer to a crypto currency (type 'bitcoin' instead of 'btc') and use the abreviation to reffer to normal currencies (type 'usd' insted of 'United States Dollar')
            
        All commands should has '$'  as a prefix.
        The commands are not case sensitive(for me write apod is the same as write APOD)"""

        await ctx.message.reply(content=message_to_be_sent)



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

    @commands.command(pass_context=True, aliases=('sayto', 'SAYTO'))
    @commands.check(CustomChecks.is_guild)
    async def say_to(self, ctx, *args):
        if len(args) > 1:
            author = ctx.author.name
            guild_name = ctx.guild.name
            message_to_send = args[0]
            user_to_send = ' '.join(args[1:])
            member = ctx.guild.get_member_named(user_to_send)

            if not member:
                await ctx.message.reply(content='That user does not exist or is not a server\'s member.')
                
            elif member.bot:
                await ctx.message.reply(content='That user is a bot. I won\'t mess with my mates 😇.')

            elif member == ctx.author:
                await ctx.message.reply(content='You can\'t use this command with yourself.')

            else:
                await ctx.message.delete()
                await ctx.send(f'{ctx.author.mention} I have sent the message, will be our secret 🤭.')
                dm_channel = await member.create_dm()
                await dm_channel.send(content=f'Hi, **{author}** from **{guild_name}** asked me to tell you **"{message_to_send}"** 🤐')
        else:
            await ctx.message.reply(content='You must especify a message and a user to send that message.')


    @say_to.error
    async def say_to_error_handler(self, ctx, error):
        """This function is for handling the errors wich will be raised if the $sayto command is not used propery.
        """
        if type(error) == commands.errors.CommandError:
            await ctx.message.reply(content=str(error))

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

    def _create_bday_message(self, today, week, month):
        """This method will help us to create the string message that will be send by next_bdays command"""

        message_to_send = ''
        if today:
            message_to_send += '\n**Today:**\n'
            message_to_send += '\n'.join(today)
        if week:
            message_to_send += '\n**In the next 7 days:**\n'
            message_to_send += '\n'.join(week)
        if month:
            message_to_send += '\n**In the current month:**\n'
            message_to_send += '\n'.join(month)

        if message_to_send:
            return message_to_send
        else:
            return 'There are no birthdays soon.'


    @commands.command(pass_context=True, aliases=('next-bdays', 'NEXT-BDAYS'))
    @commands.check(CustomChecks.is_guild)
    @commands.check(CustomChecks.is_bdays_channel)
    async def next_bdays(self, ctx):

        with open(self._bdays_data_path, 'r') as f:
            bdays_dict = json.load(f)

        server_data = bdays_dict.get(str(ctx.guild.id), None)

        if server_data:
            server_data_copy = copy.deepcopy(server_data)
            today_date = datetime.date.today()
            today_day = today_date.day
            today_month = today_date.month
            
            today_bdays = []
            week_bdays = []
            month_bdays = []

            for k, v in server_data.items():
                try:
                #if the bday is today
                    if all((v[0] == today_month, v[1] == today_day)):
                        mention = ctx.guild.get_member(int(k)).mention
                        today_bdays.append(mention)

                    #if the bday is in the next 7 days
                    #using all method to avoid use a lot of and statements

                    elif all(((v[1] - today_day) > 0, (v[1] - today_day) <= 7, v[0] == today_month)):
                        mention = ctx.guild.get_member(int(k)).mention
                        week_bdays.append(mention)
                    
                    #if the bday is in the current month
                    elif all((v[0] == today_month, today_day < v[1])):
                        mention = ctx.guild.get_member(int(k)).mention
                        month_bdays.append(mention)

                except AttributeError:
                    del server_data_copy[k]
                    continue
            
            await ctx.send(self._create_bday_message(today_bdays, week_bdays, month_bdays))

            #If the dict has changed, it will happen if someome who stored his bday has left the server and his data is still there.  
            if server_data_copy != server_data:
                bdays_dict[str(ctx.guild.id)] = server_data_copy
                with open(self._bdays_data_path, 'w') as f:
                    json.dump(bdays_dict, f)
            

        else:
            await ctx.send('This server does not have stored birthdays use "$set-bday" to store your birthday.')


    @next_bdays.error
    async def next_bdays_error_handler(self, ctx, error):
        """This function is for handling the errors wich be raised if the $next-bdays command is not used properly.
        """
        if type(error) == commands.errors.CommandError:
            await ctx.message.reply(content= str(error))
        print(error)



        

