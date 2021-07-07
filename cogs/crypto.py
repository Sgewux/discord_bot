import re
from discord.ext import commands
from cogs.bot_utilities.checks import CustomChecks
from cogs.bot_utilities.crypto_api import CryptoApi


class CryptoCommands(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self._api = CryptoApi()

	@commands.command(pass_context=True, aliases=('cprice', 'CPRICE'))
	async def get_price(self, ctx, crypto_name, currency_name):
	    currency_name = currency_name.lower()
	    crypto_name = crypto_name.lower()
	    price = self._api.get_crypto_price(crypto_name, currency_name)

	    await ctx.message.reply(content=price)

	@commands.command(pass_context=True, aliases=('ctc', 'CTC'))
	async def convert_to_crypto(self, ctx, amount: float, currency_name, crypto_name):
	    currency_name = currency_name.lower()
	    crypto_name = crypto_name.lower()
	    convertion = self._api.convert_to_crypto(currency_name, crypto_name, amount)

	    await ctx.message.reply(content=convertion)

	@commands.command(pass_context=True, aliases=('cfc', 'CFC'))
	async def convert_from_crypto(self, ctx, amount: float, crypto_name, currency_name):
	    currency_name = currency_name.lower()
	    crypto_name = crypto_name.lower()
	    convertion = self._api.convert_from_crypto(crypto_name, currency_name, amount)

	    await ctx.message.reply(content=convertion)

	@commands.command(pass_context=True, aliases=('ghp', 'GHP'))
	async def get_historical_price(self, ctx, *args):
	    date = '-'.join(args)
	    date_regex = re.compile(r'\d{4}-\d{2}-\d{2}')

	    if date_regex.search(date):
	        year, month, day = date.split('-')
	        if CustomChecks.is_valid_date(int(month), int(day), year=int(year)):
	            price = self._api.get_historical_price(date)
	            await ctx.message.reply(content=price)
	        else:
	            await ctx.message.reply(content='It is not a valid date.')
	    else:
	        await ctx.message.reply(content='It is not a date, i\'m not dumb 😑')
