from typing import Union

import requests
from brownie import TrustedWrapperV2, config


class IndexCalculator:
    """
    A class for calculating the index value of a wrapped non-fungible token (WNFT)
    which contains various assets. It uses an external API to fetch the latest prices
    for the underlying assets in USD.

    Attributes:
        price_provider (str): The API URL to fetch the latest asset prices.
        index_assets_config (dict): A dictionary containing the configuration of the index assets.
        wnft_contract_address (str): The contract address for the WNFT.
        wnft_id (id): The identification number of the specific WNFT.
        saft_wrapper_address (str): The address of the SAFT wrapper contract.
    """
    def __init__(
            self, 
            price_provider,
            index_assets_config,
            wnft_contract_address, 
            wnft_id, saft_wrapper_address, 
        ):
        self.price_provider: str = price_provider
        self.index_assets_config: dict = index_assets_config
        self.wnft_contract_address: str = wnft_contract_address
        self.wnft_id: id = wnft_id
        self.saft_wrapper_address: str = saft_wrapper_address

    def _fetch_price(self, token_symbol: str) -> Union[int, str]:
        """
        Fetches the current price of the given token symbol in USD.

        This private method is responsible for making the API call to the price provider
        and retrieving the latest price for a specified token symbol.

        Args:
            token_symbol (str): The symbol of the token to fetch the price for.

        Returns:
            Union[int, str]: The price of the token if successful, otherwise an error message.
        """
        parameters = {
            'symbol': token_symbol,
            'convert': 'USD'
        }
        headers = {
            'X-CMC_PRO_API_KEY': config['price_provider'].get('api_key')
        }
        response = requests.get(self.price_provider, params=parameters, headers=headers)
        data = response.json()
        if token_symbol in data['data']:
            return data['data'][token_symbol]['quote']['USD']['price']
        else:
            return f"Error fetching price for {token_symbol}"

    def _get_index_assets_config_with_price(self, index_assets_config: list) -> dict:
        """
        Augments the index assets configuration with the latest prices fetched from the API.

        Args:
            index_assets_config (list): A list of token configurations to augment with price information.

        Returns:
            dict: The updated index assets configuration with current price data.
        """
        for token in index_assets_config:
            ticker = token['ticker']
            token_price_in_usd: Union[int, str] = self._fetch_price(ticker)
            token['price'] = token_price_in_usd
        return index_assets_config

    def _get_index_amount(self) -> dict:
        """
        Retrieves the amount of each asset in the index.

        Uses the saft_wraper_contract to get information about the collateral
        within the WNFT and calculates the token amount for each.

        Returns:
            dict: A dictionary mapping token addresses to their respective amounts in the index.
        """
        token_decimal = 1e18
        index_amount = {}
        saft_wraper_contract = TrustedWrapperV2.at(self.saft_wrapper_address)
        wnft = saft_wraper_contract.getWrappedToken(
            self.wnft_contract_address,
            self.wnft_id
        )
        collateral: list = wnft[1]
        for token in collateral:
            token_address = token[0][1]
            token_amount = token[2]
            index_amount[token_address] = token_amount / token_decimal

        return index_amount

    def _get_final_config(self, index_assets_config_with_price: list, index_amount: dict) -> dict:
        """
        Finalizes the configuration for the index assets by calculating the total price.

        This method combines the price per unit with the amount for each asset to determine
        the total price of that asset within the index.

        Args:
            index_assets_config_with_price (list): The list of asset configurations with their respective prices.
            index_amount (dict): A dictionary containing the amount of each asset in the index.

        Returns:
            dict: The final configuration with the total price for each asset included in the index.
        """
        for token in index_assets_config_with_price:
            token_amount = index_amount[token['address']]
            token['amount'] = token_amount
            token_price_in_usd_per_unit = token['price']
            total_price = token_amount * token_price_in_usd_per_unit
            token['total_price'] = total_price
        return index_assets_config_with_price

    def get_calculated_index(self) -> dict:
        """
        Calculates the final index configuration.

        This method orchestrates the whole process of fetching prices, calculating the amount
        of assets, and combining this information to produce the final index configuration with
        updated prices and total values.

        Returns:
            dict: The final calculated index configuration.
        """
        index_assets_config_with_price = self._get_index_assets_config_with_price(self.index_assets_config)
        index_amount = self._get_index_amount()
        final_index_config =  self._get_final_config(index_assets_config_with_price, index_amount)
        return final_index_config