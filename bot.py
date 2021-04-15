import discord
import asyncio
from discord.ext import commands
from bot_utilities.weather_scraper import WeatherScraper

client = discord.Client()
bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    print(f'We are logged {bot.user}')


#@bot.event
#async def on_message(message):
 #   if message.author != bot.user:
  #      if message.content.startswith('$sayhi'):
   #         await message.channel.send(f'Hi {message.author.mention}! How r u?')
    #else:
     #   return None


@bot.event
async def on_typing(channel, user, when):
    if type(channel) == discord.channel.TextChannel:
        if user.id == channel.guild.owner_id:
            await channel.send('Shhh 🤫 The owner is typing right know.')
    else:
        return None


#@bot.command(pass_context=True)
#async def help(ctx):
 #   message_to_be_sent = """Hi 👋, my name is Diego Norrea 
  #  I'm a Discord bot and i have the following commands:
   # -Weather: Given a place i will tell you the weather and temperature of that place."""

    #await ctx.send(message_to_be_sent)

@bot.command(pass_context=True)
async def weather(ctx, place):
    print('lmao')
    await ctx.send(f'Weather in {place} is currently: {WeatherScraper(place).get_temperature_and_weather()}')


if __name__ == '__main__':
    bot.run('ODMwNDU3MjA2MTcxMjM4NDEw.YHG9iw.bt0lKIAnQCl8XUiG7d0YVc3HdAE')
