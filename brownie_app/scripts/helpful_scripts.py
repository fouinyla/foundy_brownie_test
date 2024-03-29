import os

from brownie import accounts, config, network

FORKED_LOCAL_ENVIRENMENTS = ['mainnet-fork', 'mainnet-fork-dev', 'mumbai-fork-dev', 'polygon-fork-dev']
LOCAL_BLOCKCHAIN_ENVIRENMENTS = ['development', 'ganache-local']


def get_account(account_label='main'):
    if(
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRENMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRENMENTS
    ):
        account = accounts[0] if account_label == 'main' else accounts[1]
        return account
    return accounts.add(config['wallets'][account_label]['from_key'])

def get_file_path(file_name: str) -> str:
    """
    Constructs a file path based on the current working directory and the given file name.

    The function checks the current directory to determine the correct path for the file.
    It specifically looks to differentiate between a 'server_app' directory and a 'brownie_app'
    directory to construct the appropriate file path. If the current directory is not recognized
    as either, the function will use an environment variable "FILES_DIRECTORY" to construct the path.

    Args:
        file_name (str): The name of the file for which to construct the path.

    Returns:
        str: The full path to the file.
    """
    # current_dir = os.path.abspath(os.curdir)
    # if 'server_app' in current_dir:
    #     return f'{current_dir}/src/{file_name}'
    # else:
    #     replaced_cur_dir = current_dir.replace('brownie_app', os.getenv("FILES_DIRECTORY"))
    #     return f'{replaced_cur_dir}/{file_name}'

    return f'../static/{file_name}'

