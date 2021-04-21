import os
import dotenv
import discord
import asyncio
from discord.ext import commands
from bot_utilities.nasa_api import NasaApi
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
    I'm a Discord bot and i have the following commands:
        -weather: Given a place i will tell you the weather and temperature of that place.
        -APOD: I will send the Astronomy Picture Of the Day.
        -MRP: I will send a random picture taken by the Curiosity mars rover.

        All commands should has as a prefix '$'."""

    await ctx.send(message_to_be_sent)


@bot.command(pass_context=True)
async def weather(ctx, *place):
    place = ''.join(place)
    await ctx.send(f'Weather in {place} is currently: {WeatherScraper(place).get_temperature_and_weather()}')


@bot.command(pass_context=True, name='APOD')
async def astro_picture(ctx):
    apod = NasaApi().get_apod()

    if apod:
        await ctx.send(f'Description 👨‍🚀:\n {apod[0]}\n {apod[1]}')
    else:
        await ctx.send('Something went wrong :(')


@bot.command(pass_context=True, name='MRP')
async def rover_photo(ctx):
    rover_photo = NasaApi().get_mars_rover_photo()

    if rover_photo:
        await ctx.send(f'{rover_photo[0]}\nThis photo was taken in: {rover_photo[1]}\nCamera name: {rover_photo[2]}')
    else:
        await ctx.send('Something went wrong :(')


if __name__ == '__main__':
    bot.run(TOKEN)
