from brownie import Wei


def get_amount_wei(amount: int, decimals: int):
    """
    Converts an amount of cryptocurrency to wei based on the specified number of decimals.

    Args:
        amount (int): The amount of cryptocurrency.
        decimals (int): The number of decimals the cryptocurrency uses.

    Returns:
        Wei: An object representing the amount in wei.

    Example:
        For an ERC-20 token with 18 decimals, calling get_amount_wei(1, 18) will return
        the Wei equivalent of 1 token.
    """
    amount_with_decimals = amount * 10 ** decimals
    return Wei(amount_with_decimals)