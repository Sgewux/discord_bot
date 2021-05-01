import os
import re
import dotenv
import discord
import asyncio
import datetime
from discord.ext import commands
from bot_utilities.nasa_api import NasaApi
from bot_utilities.crypto_commands import CryptoCommands
from bot_utilities.weather_scraper import WeatherScraper

dotenv.load_dotenv()
TOKEN = os.getenv('DISCORD_API_TOKEN')
bot = commands.Bot(command_prefix='$', help_command=None)

@bot.event
async def on_ready():
    print(f'We are logged {bot.user}')


@bot.event
async def on_typing(channel, user, when):
    if type(channel) == discord.channel.TextChannel:
        if user.id == channel.guild.owner_id:
            await channel.send('Shhh 🤫 The owner is typing right know.')
    else:
        return None


@bot.command(pass_context=True)
async def help(ctx):
    message_to_be_sent = """
    Hi 👋, my name is Diego Norrea 
    I'm a Discord bot 🤖 and i have the following commands:

        General commands 🌎:
            -weather: Given a place i will tell you the weather and temperature of that place.
            -HMD: To know how many days you have been on this server.

        Space commands 🚀:
            -APOD: I will send the Astronomy Picture Of the Day.
            -MRP: I will send a random picture taken by the Curiosity mars rover.
            -MRPD: I will send a photo taken by the Curiosity mars rover in date with the year month day format given by you
            (use blank spaces to split the values).

        Crypto commands 💲:
            -cprice: Given a cryptocurrency name (bitcoin for example) and a normal currency (usd for example) i will send you the current
            price of that currency.
            -CTC: Given a normal currency name, cryptocurrency name and an amount i will Convert To Crypto that amount.
            -CFC: Given a cryptocurrency name, normal currency name and an amount i will Convert From Crypto that amount.
            Use the full name to reffer to a crypto currency (type 'bitcoin' instead of 'btc') and use the abreviation to reffer to normal
            currencies (type 'usd' insted of 'United States Dollar')

        All commands should has '$'  as a prefix.
        The commands are not case sensitive(for me write apod is the same as write APOD)"""

    await ctx.message.reply(content=message_to_be_sent)


@bot.command(pass_context=True, aliases=('weather', 'WEATHER'))
async def get_weather(ctx, *place):
    place = ''.join(place)
    await ctx.message.reply(content=f'Weather in {place} is currently: {WeatherScraper(place).get_temperature_and_weather()}')


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


@bot.command(pass_context=True, aliases=('HMD', 'hmd'))
async def time_belonging(ctx):
    if type(ctx.author) == discord.member.Member:
        join_date = ctx.author.joined_at
        current_date = datetime.datetime.now()
        delta = current_date - join_date
        await ctx.message.reply(content=f'You\'ve been on this server for {delta.days} days!')
    else:
        return None


@bot.command(pass_context=True, aliases=('MRPD', 'mrpd'))
async def rover_photo_by_date(ctx, *args):
    date = '-'.join(args)
    date_regex = re.compile('\d{4}-\d{1,2}-\d{1,2}')
    
    if date_regex.search(date):
        photo_url = NasaApi().get_rover_photo_by_date(date)
        await ctx.message.reply(content=photo_url)
    else:
        await ctx.message.reply(content='It is not a date, i\'m not dumb 😑')


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


if __name__ == '__main__':
    bot.run(TOKEN)
