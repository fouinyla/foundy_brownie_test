from brownie import FINDEX, config, network
from brownie.network import web3 as w3
from brownie.network.transaction import TransactionReceipt
from web3.middleware.geth_poa import geth_poa_middleware
from scripts.helpful_scripts import get_account
from time import sleep


def deploy_dynamic_index():
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    account = get_account(account_label='worker')
    dynamic_index = FINDEX.deploy(
        {'from': account, "priority_fee": 35000000000},
        publish_source=config['networks'][network.show_active()].get('verify')
    )

    print(f'Contract {dynamic_index._name} deployed to: {dynamic_index.address}')
    return dynamic_index


def verify_deployed_contract(contract_address: str) -> None:
    token_contract = FINDEX.at(contract_address)
    FINDEX.publish_source(token_contract)


def create_collectible(contract_address: str) -> TransactionReceipt:
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    token_contract = FINDEX.at(contract_address)
    account = get_account(account_label='worker')
    new_item_id: TransactionReceipt = token_contract.createCollectible({'from': account})

    return new_item_id


def main():
    # dynamic_index = deploy_dynamic_index()
    # verify_deployed_contract(contract_address=dynamic_index.address)
    # cc = create_collectible(contract_address=dynamic_index.address)

    # verify_deployed_contract(contract_address="0x979Ee4b9ed42B01D4Eaf07c65C604272104CbA2C")
    # cc = create_collectible(contract_address="0x979Ee4b9ed42B01D4Eaf07c65C604272104CbA2C")
    pass
    