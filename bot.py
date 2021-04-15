import discord
import asyncio
from discord.ext import commands
from bot_utilities import astronomy_picture
from bot_utilities.weather_scraper import WeatherScraper


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
        -APOD: I'll give you the Astronomy Picture Of the Day.

        All commands should has as a prefix '$'."""

    await ctx.send(message_to_be_sent)


@bot.command(pass_context=True)
async def weather(ctx, place):
    await ctx.send(f'Weather in {place} is currently: {WeatherScraper(place).get_temperature_and_weather()}')


@bot.command(pass_context=True, name='APOD')
async def astro_image(ctx):
    text_and_pic = astronomy_picture.get_astronomy_image()

    if text_and_pic:
        await ctx.send(f'Description:\n {text_and_pic[0]}\n {text_and_pic[1]}')
    else:
        await ctx.send('Something went wronf :(')


if __name__ == '__main__':
    bot.run('ODMwNDU3MjA2MTcxMjM4NDEw.YHG9iw.bt0lKIAnQCl8XUiG7d0YVc3HdAE')
