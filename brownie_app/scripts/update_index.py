from brownie import DINDEX
from scripts.helpful_scripts import get_account


def update_index(dindex_contact_address: str, ipfs_metadata_link: str, token_id: int):
    account = get_account(account_label='worker')
    ipfs_metadata_link
    dindec_contract = DINDEX.at(dindex_contact_address)
    tx = dindec_contract.setTokenURI(
        token_id,
        ipfs_metadata_link,
        {"from": account}
    )
    tx.wait(1)
    return tx 