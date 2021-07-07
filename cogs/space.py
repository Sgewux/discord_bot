import re
from discord.ext import commands
from cogs.bot_utilities.nasa_api import NasaApi
from cogs.bot_utilities.checks import CustomChecks


class SpaceCommands(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self._api = NasaApi()

	@commands.command(pass_context=True, aliases=('APOD', 'apod'))
	async def astronomy_picture_of_the_day(self, ctx):
		"""Gives us the astronomy picture of the day"""
		apod = self._api.get_apod()

		if apod:
			await ctx.send(f'Description 👨‍🚀:\n {apod[0]}\n {apod[1]}')
		else:
			await ctx.send('Something went wrong :(')

	@commands.command(pass_context=True,  aliases=('MRP', 'mrp'))
	async def rover_photo(self, ctx):
		"""Gives us a random photo taken by the mars rover"""

		rover_photo = self._api.get_mars_rover_photo()

		if rover_photo: 
			await ctx.message.reply(content=f'{rover_photo[0]}\nThis photo was taken in: {rover_photo[1]}\nCamera name: {rover_photo[2]}') 
		else:
			await ctx.message.reply(content='Something went wrong :( \nPlease try again.')

	@commands.command(pass_context=True, aliases=('MRPD', 'mrpd'))
	async def rover_photo_by_date(self, ctx, *args):
		date = '-'.join(args)
		date_regex = re.compile(r'\d{4}-\d{1,2}-\d{1,2}')

		if date_regex.search(date):
			year, month, day = date.split('-')
			if CustomChecks.is_valid_date(int(month), int(day), year=int(year)):
				photo_url = self._api.get_rover_photo_by_date(date)
				await ctx.message.reply(content=photo_url)
			else:
				await ctx.message.reply(content='That is an unexistent date.')
		else:
			await ctx.message.reply(content='That is not a date i\'m not dumb 😑')


