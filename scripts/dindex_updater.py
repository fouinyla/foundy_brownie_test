from brownie import config
from scripts.create_index_image import get_generated_index_image_name
from scripts.index_calculator import IndexCalculator
from scripts.ipfs_loader import IPFSLoader
from scripts.OpenAI import get_generated_image_name
from scripts.update_index import update_index


def main():

    # 1.Calculate index
    index_assets_config = [
        {'ticker': 'MATIC', 'address': '0x0000000000000000000000000000000000000000', 'amount': 1, 'price': None, 'total_price': None},
        {'ticker': 'NIFTSY', 'address': '0x432cdbC749FD96AA35e1dC27765b23fDCc8F5cf1', 'amount': 1, 'price': None, 'total_price': None},
    ]
    index_calculator = IndexCalculator(
        price_provider=config['price_provider'].get('url'),
        index_assets_config=index_assets_config,
        # current
        wnft_contract_address='0x0bfede1f408164884e3cc90a30587e55f3147ba9',
        wnft_id=2,

        # wnft_contract_address='0x0bfede1f408164884e3cc90a30587e55f3147ba9',
        # wnft_id=3,
        # wnft_contract_address='0xFb453ebA20Dc4598bb77A22747B0BCc971B5630B',
        saft_wrapper_address='0x018Ab23bae3eD9Ec598B1239f37B998fEDB75af3',
    )

    calculated_index: dict = index_calculator.get_calculated_index()
    print(f'Calculated index:\n{calculated_index}')

    # 2.Build image
    image_prompt: str = config['image_generator'].get('prompt')
    generated_image_name: str = get_generated_image_name(image_prompt)

    generated_index_image_path, generated_index_image_name = get_generated_index_image_name(
        image_name=generated_image_name, 
        final_index_config=calculated_index
    )
    print(f'Image {generated_index_image_name} stored to:{generated_index_image_path}')

    # 3.Upload metadata json to IPFS
    ipfs_loader = IPFSLoader()
    ipfs_metadata_link: str = ipfs_loader.get_uploadet_metadata_link(
        generated_index_image_path, generated_index_image_name
    )
    print(f'NFT medata for update:\n{ipfs_metadata_link}')

    # 4.Update URI Metadata
    update_transaction = update_index(
        dindex_contact_address='0x4Be69b3FFE8de177aAd2848715037848140C418F',
        # dindex_contact_address='0x0457c7395793f5Dd0B339e3AA975E11877eA4ecf',
        ipfs_metadata_link=ipfs_metadata_link,
        token_id=1
    )
    print(f'Update transaction: {update_transaction}')




# (
#     ((0, '0x0000000000000000000000000000000000000000'), 0, 0), 
#     (
#         (
#             (1, '0x0000000000000000000000000000000000000000'), 0, 1000000000000000000
#         ), 
#         (
#             (2, '0x432cdbC749FD96AA35e1dC27765b23fDCc8F5cf1'), 0, 1000000000000000000
#         )
#     ), 
#     '0x0000000000000000000000000000000000000000', 
#     (
#         (0x00, 1, '0x0000000000000000000000000000000000000000'),
#     ), 
#     (), 
#     (
#         ('0xD2f4D892fb7615989A73667aA8B477a2BFCfa6C9', 10000),
#     ), 
#     0x0000
# )