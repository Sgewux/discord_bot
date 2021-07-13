import os
import dotenv
import discord
from discord.ext import commands
from cogs.space import SpaceCommands
from cogs.crypto import CryptoCommands
from cogs.general import GeneralCommands

dotenv.load_dotenv()
TOKEN = os.getenv('DISCORD_API_TOKEN')
intents = discord.Intents().all()
bot = commands.Bot(command_prefix='$', help_command=None, intents=intents)

@bot.event
async def on_ready():
    print(f'We are logged {bot.user}')
#@bot.event
#async def on_typing(channel, user, when):
 #   if type(channel) == discord.channel.TextChannel:
  #      if user.id == channel.guild.owner_id:
   #         await channel.send('Shhh 🤫 The owner is typing right know.')
    #else:
     #   return None
bot.add_cog(SpaceCommands(bot))
bot.add_cog(CryptoCommands(bot))
bot.add_cog(GeneralCommands(bot))

if __name__ == '__main__':
    bot.run(TOKEN)

