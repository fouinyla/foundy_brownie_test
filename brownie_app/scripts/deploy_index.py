from brownie import DINDEX, config, network
from scripts.helpful_scripts import get_account


def deploy_dynamic_index():
    account = get_account(account_label='worker')
    dynamic_index = DINDEX.deploy(

        {'from': account},
        publish_source=config['networks'][network.show_active()].get('verify')
    )

    print(f'Contract {dynamic_index._name} deployed to: {dynamic_index.address}')
    return dynamic_index



def main():
    deploy_dynamic_index()