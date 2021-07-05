import os
import re
import json
import copy
import dotenv
import discord
import asyncio
import datetime
from discord.ext import commands
from bot_utilities.nasa_api import NasaApi
from bot_utilities.checks import CustomChecks
from bot_utilities.crypto_commands import CryptoCommands
from bot_utilities.weather_scraper import WeatherScraper

dotenv.load_dotenv()
TOKEN = os.getenv('DISCORD_API_TOKEN')
intents = discord.Intents().all()
bot = commands.Bot(command_prefix='$', help_command=None, intents=intents)

@bot.event
async def on_ready():
    print(f'We are logged {bot.user}')


@bot.event
async def on_member_join(member):
    guild = bot.get_guild(member.guild.id)
    user_id = member.id
    user_mention = member.mention
    welcomes_channel = None
    for channel in guild.text_channels:
        if 'welcome' in channel.name:
            welcomes_channel = channel

    if welcomes_channel:
        with open('./data/members_who_left.json', 'r') as f:
            members_who_left = json.load(f)
        
        server_data = members_who_left.get(str(guild.id), None)

        if server_data:
            if user_id in server_data:
                await welcomes_channel.send(f'Welcome back {user_mention}! I hope you won\'t be planning to leave the server this time 🤨.')
            else:
                await welcomes_channel.send(f'Welcome to this server {user_mention}! I hope you have a good time here 😄.')
        else:
            await welcomes_channel.send(f'Welcome to this server {user_mention}! I hope you have a good time here 😄.')


@bot.event
async def on_member_remove(member):
    guild = bot.get_guild(member.guild.id)
    user_id = member.id

    with open('./data/members_who_left.json', 'r') as f:
        members_who_left = json.load(f)

    server_data = members_who_left.get(str(guild.id), None)

    if not server_data:
        server_data = [user_id]
    else:
        if user_id not in server_data:
            server_data.append(user_id)
    
    members_who_left[str(guild.id)] = server_data

    with open('./data/members_who_left.json', 'w') as f:
        json.dump(members_who_left, f)

        
#@bot.event
#async def on_typing(channel, user, when):
 #   if type(channel) == discord.channel.TextChannel:
  #      if user.id == channel.guild.owner_id:
   #         await channel.send('Shhh 🤫 The owner is typing right know.')
    #else:
     #   return None



#general
@bot.command(pass_context=True)
async def help(ctx):
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


@bot.command(pass_context=True, aliases=('weather', 'WEATHER'))
async def get_weather(ctx, *place):
    place = ''.join(place)
    await ctx.message.reply(content=f'Weather in {place} is currently: {WeatherScraper(place).get_temperature_and_weather()}')


@bot.command(pass_context=True, aliases=('HMD', 'hmd'))
async def time_belonging(ctx):
    if type(ctx.author) == discord.member.Member:
        join_date = ctx.author.joined_at
        current_date = datetime.datetime.now()
        delta = current_date - join_date
        await ctx.message.reply(content=f'You\'ve been on this server for {delta.days} days!')
    else:
        return None


@bot.command(pass_context=True, aliases=('sayto', 'SAYTO'))
@commands.check(CustomChecks.is_guild)
async def say_to(ctx, *args):
    if len(args) > 1:
        author = ctx.author.name
        guild_name = ctx.guild.name
        message_to_send = args[0]
        user_to_send = ' '.join(args[1:])
        member = ctx.guild.get_member_named(user_to_send)

        if not member:
            await ctx.message.reply(content='That user does not exist or is not a server\'s member.')
            
        elif member.bot:
            await ctx.message.reply(content='That user is a bot. I won\'t mess with my parthners 😇.')

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
async def say_to_error_handler(ctx, error):
    """This function is for handling the errors wich will be raised if the $sayto command is not used propery.
    """
    await ctx.message.repy(content=str(error))


@bot.command(pass_context=True, aliases=('set-bday', 'SET-BDAY'))
@commands.check(CustomChecks.is_guild)
@commands.check(CustomChecks.is_bdays_channel)
async def set_bday(ctx, month: int, day: int):

    guild_id = str(ctx.guild.id)
    user_id = str(ctx.author.id)

    with open('./data/birth_days.json', 'r') as f:
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

    with open('./data/birth_days.json', 'w') as f:
        json.dump(bdays_dict, f)

    await ctx.message.reply(content="Birhtday saved 😉.")


@set_bday.error
async def set_bday_error_handler(ctx, error):
    """This function is for handling the errors wich be raised if the $set-bday command is not used properly.
    """
    await ctx.message.reply(content= str(error))


@bot.command(pass_context=True, aliases=('next-bdays', 'NEXT-BDAYS'))
@commands.check(CustomChecks.is_guild)
@commands.check(CustomChecks.is_bdays_channel)
async def next_bdays(ctx):

    with open('./data/birth_days.json', 'r') as f:
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
                if v[0] == today_month and v[1] == today_day:
                    mention = ctx.guild.get_member(int(k)).mention
                    today_bdays.append(mention)

                #if the bday is in the next 7 days
                elif (v[1] - today_day) > 0 and (v[1] - today_day) <= 7  and v[0] == today_month:
                    mention = ctx.guild.get_member(int(k)).mention
                    week_bdays.append(mention)
                
                #if the bdat is in the current month
                elif v[0] == today_month and today_day < v[1]:
                    mention = ctx.guild.get_member(int(k)).mention
                    month_bdays.append(mention)

            except AttributeError:
                del server_data_copy[k]
                continue
        
        message_to_send = ''

        if today_bdays:
            message_to_send += '\n**Today:**\n'
            message_to_send += '\n'.join(today_bdays)
        if week_bdays:
            message_to_send += '\n**In the next 7 days:**\n'
            message_to_send += '\n'.join(week_bdays)
        if month_bdays:
            message_to_send += '\n**In the current month:**\n'
            message_to_send += '\n'.join(month_bdays)


        if message_to_send:
            await ctx.send(message_to_send)
        else:
            await ctx.send('There are no birthdays soon.')

        #If the dict has changed, it will happen if someome who stored his bday has left the server and his data is still there.  
        if server_data_copy != server_data:
            bdays_dict[str(ctx.guild.id)] = server_data_copy
            with open('./data/birth_days.json', 'w') as f:
                json.dump(bdays_dict, f)
        

    else:
        await ctx.send('This server does not have stored birthdays use "$set-bday" to store your birthday.')


@next_bdays.error
async def next_bdays_error_handler(ctx, error):
    """This function is for handling the errors wich be raised if the $next-bdays command is not used properly.
    """
    await ctx.message.reply(content= str(error))



#nasa
@bot.command(pass_context=True, aliases=('APOD', 'apod'))
async def astro_picture(ctx):
    apod = NasaApi().get_apod()

    if apod:
        await ctx.send(f'Description 👨‍🚀:\n {apod[0]}\n {apod[1]}')
    else:
        await ctx.send('Something went wrong :(')


@bot.command(pass_context=True,  aliases=('MRP', 'mrp'))
async def rover_photo(ctx):
    rover_photo = NasaApi().get_mars_rover_photo()

    if rover_photo: 
        await ctx.message.reply(content=f'{rover_photo[0]}\nThis photo was taken in: {rover_photo[1]}\nCamera name: {rover_photo[2]}') 
    else:
        await ctx.message.reply(content='Something went wrong :( \nPlease try again.')


@bot.command(pass_context=True, aliases=('MRPD', 'mrpd'))
async def rover_photo_by_date(ctx, *args):
    date = '-'.join(args)
    date_regex = re.compile(r'\d{4}-\d{1,2}-\d{1,2}')
    
    if date_regex.search(date):
        year, month, day = date.split('-')
        if CustomChecks.is_valid_date(int(month), int(day), year=int(year)):
            photo_url = NasaApi().get_rover_photo_by_date(date)
            await ctx.message.reply(content=photo_url)
        else:
            await ctx.message.reply(content='That is an unexistent date.')

    else:
        await ctx.message.reply(content='That is not a date, i\'m not dumb 😑')




#crypto
@bot.command(pass_context=True, aliases=('cprice', 'CPRICE'))
async def get_price(ctx, crypto_name, currency_name):
    currency_name = currency_name.lower()
    crypto_name = crypto_name.lower()
    price = CryptoCommands().get_crypto_price(crypto_name, currency_name)

    await ctx.message.reply(content=price)


@bot.command(pass_context=True, aliases=('ctc', 'CTC'))
async def conv_to_crypto(ctx, amount: float, currency_name, crypto_name):
    currency_name = currency_name.lower()
    crypto_name = crypto_name.lower()
    convertion = CryptoCommands().convert_to_crypto(currency_name, crypto_name, amount)

    await ctx.message.reply(content=convertion)


@bot.command(pass_context=True, aliases=('cfc', 'CFC'))
async def conv_from_crypto(ctx, amount: float, crypto_name, currency_name):
    currency_name = currency_name.lower()
    crypto_name = crypto_name.lower()
    convertion = CryptoCommands().convert_from_crypto(crypto_name, currency_name, amount)

    await ctx.message.reply(content=convertion)


@bot.command(pass_context=True, aliases=('ghp', 'GHP'))
async def get_h_price(ctx, *args):
    date = '-'.join(args)
    date_regex = re.compile('\d{4}-\d{2}-\d{2}')

    if date_regex.search(date):
        price = CryptoCommands().get_historical_price(date)
        await ctx.message.reply(content=price)
    else:
        await ctx.message.reply(content='It is not a date, i\'m not dumb 😑')

#

if __name__ == '__main__':
    bot.run(TOKEN)

