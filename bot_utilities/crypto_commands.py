import json
import requests

class CryptoCommands(object):

    def __init__(self):
        self._api_url = 'https://api.coingecko.com/api/v3/coins/{0}?localization=false&tickers=false&community_data=false&developer_data=false&sparkline=false%22'

    def get_crypto_price(self, name_crypto, name_currency):
        url = self._api_url.format(name_crypto)
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = json.loads(response.text)
            price = data['market_data']['current_price'][name_currency]

            return f'1 {name_crypto} = {price} {name_currency}'

        except requests.HTTPError:
            return f'Sorry, that cryptocurrency doesn\'t exist or i dont have info about it :('

        except KeyError:
            return f'Sorry, i didn\'t foud {name_crypto}\'s price in {name_currency} :('

    
    def convert_to_crypto(self, name_currency, name_crypto, amount):
        url = self._api_url.format(name_crypto)
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = json.loads(response.text)
            price = data['market_data']['current_price'][name_currency]
            converted_value = (amount/price)
        
            return f'{amount} {name_currency} = {converted_value} {name_crypto}'
        
        except requests.HTTPError:
            return f'Sorry, that cryptocurrency doesn\'t exist or i dont have info about it :('

        except KeyError:
            return f'Sorry, i coudn\'t convert {name_currency} to {name_crypto}. Try with another currency :('


    def convert_from_crypto(self, name_crypto, name_currency, amount):
        url = self._api_url.format(name_crypto)
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = json.loads(response.text)
            price = data['market_data']['current_price'][name_currency]
            converted_value = (amount * price)
        
            return f'{amount} {name_crypto} = {converted_value} {name_currency}'
        
        except requests.HTTPError:
            return f'Sorry, that cryptocurrency doesn\'t exist or i dont have info about it :('

        except KeyError:
            return f'Sorry, i coudn\'t convert {name_crypto} to {name_currency}. Try with another currency :('


