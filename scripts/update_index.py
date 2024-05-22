from brownie import FINDEX
from brownie.network import web3 as w3
from web3.middleware.geth_poa import geth_poa_middleware
from scripts.helpful_scripts import get_account


def update_index(dindex_contact_address: str, ipfs_metadata_link: str, token_id: int):
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    account = get_account(account_label='worker')
    ipfs_metadata_link
    dindec_contract = FINDEX.at(dindex_contact_address)
    tx = dindec_contract.setTokenURI(
        token_id,
        ipfs_metadata_link,
        {"from": account}
    )
    tx.wait(1)
