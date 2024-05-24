from brownie import config
from scripts.create_index_image import get_generated_index_image_name
from scripts.index_calculator import IndexCalculator
from scripts.ipfs_loader import IPFSLoader
from scripts.OpenAI import get_generated_image_name
from scripts.update_index import update_index


def main():

    # 1.Calculate index
    index_assets_config = [
        {'ticker': '1INCH', 'address': '0x9c2C5fd7b07E95EE044DDeba0E97a665F142394f', 'amount': 3.205, 'price': 0.39, 'total_price': 1.24995},
        {'ticker': 'UNI', 'address': '0xb33EaAd8d922B1083446DC23f610c2567fB5180f', 'amount': 0.165, 'price': 7.58, 'total_price': 1.2507},
        {'ticker': 'MATIC', 'address': '0x0000000000000000000000000000000000000000', 'amount': 4.515, 'price': 0.72, 'total_price': 3.2508},
        {'ticker': 'WBTC', 'address': '0x1BFD67037B42Cf73acF2047067bd4F2C47D9BfD6', 'amount': 0.0001125, 'price': 66969, 'total_price': 7.5340125},
        {'ticker': 'AVAX', 'address': '0x2C89bbc92BD86F8075d1DEcc58C7F4E0107f286b', 'amount': 0.0675, 'price': 37.14, 'total_price': 2.50695},
        {'ticker': 'LINK', 'address': '0x53E0bca35eC356BD5ddDFebbD1Fc0fD03FaBad39', 'amount': 0.1075, 'price': 16.16, 'total_price': 1.7372},
        {'ticker': 'MANA', 'address': '0xA1c57f48F0Deb89f569dFbE6E2B7f46D33606fD4', 'amount': 1.705, 'price': 0.44, 'total_price': 0.7502},
        {'ticker': 'CRV', 'address': '0x172370d5Cd63279eFa6d502DAB29171933a610AF', 'amount': 1.705, 'price': 0.44, 'total_price': 0.7502},
        {'ticker': 'AAVE', 'address': '0xD6DF932A45C0f255f85145f286eA0b292B21C90B', 'amount': 0.01, 'price': 89.15, 'total_price': 0.8915},
        {'ticker': 'WETH', 'address': '0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619', 'amount': 0.001625, 'price': 3100, 'total_price': 5.0375},
    ]
    # index_assets_config = [
    #     {'ticker': 'MATIC', 'address': '0x0000000000000000000000000000000000000000', 'amount': 1, 'price': None, 'total_price': None},
    #     {'ticker': 'NIFTSY', 'address': '0x432cdbC749FD96AA35e1dC27765b23fDCc8F5cf1', 'amount': 1, 'price': None, 'total_price': None},
    # ]
    index_calculator = IndexCalculator(
        price_provider=config['price_provider'].get('url'),
        index_assets_config=index_assets_config,
        # current
        #  wnft_contract_address='0x0bfede1f408164884e3cc90a30587e55f3147ba9',
        # wnft_id=2,
        wnft_contract_address='0x347d5125a7b5b8c14400bfc8d8230014b9cd3033',
        wnft_id=25,

        # wnft_contract_address='0x0bfede1f408164884e3cc90a30587e55f3147ba9',
        # wnft_id=3,
        # wnft_contract_address='0xFb453ebA20Dc4598bb77A22747B0BCc971B5630B',
        saft_wrapper_address='0x018Ab23bae3eD9Ec598B1239f37B998fEDB75af3',
    )

    calculated_index: dict = index_calculator.get_calculated_index()
    print(f'Calculated index:\n{calculated_index}')
    index_price: float = sum([token["total_price"] for token in calculated_index])
    print("index_price: ", index_price)

    # 2.Build image
    image_prompt: str = config['image_generator'].get('prompt')
    generated_image_name: str = get_generated_image_name(image_prompt)

    generated_index_image_path, generated_index_image_name = get_generated_index_image_name(
        image_name=generated_image_name, 
        final_index_config=calculated_index
    )
    print(f'Image {generated_index_image_name} stored to:{generated_index_image_path}')

    # # 3.Upload metadata json to IPFS
    # ipfs_loader = IPFSLoader()
    # ipfs_metadata_link: str = ipfs_loader.get_uploadet_metadata_link(
    #     "test", "test"
    # )
    # print(f'NFT medata for update:\n{ipfs_metadata_link}')

    # # 4.Update URI Metadata
    # update_transaction = update_index(
    #     dindex_contact_address='0x979Ee4b9ed42B01D4Eaf07c65C604272104CbA2C',
    #     # dindex_contact_address='0x0457c7395793f5Dd0B339e3AA975E11877eA4ecf',
    #     ipfs_metadata_link=ipfs_metadata_link,
    #     token_id=0
    # )
    # # print(f'Update transaction: {update_transaction}')




(
    ((0, '0x0000000000000000000000000000000000000000'), 0, 0), 
    (
        ((1, '0x0000000000000000000000000000000000000000'), 0, 1000000000000000000), 
        ((2, '0x432cdbC749FD96AA35e1dC27765b23fDCc8F5cf1'), 0, 1000000000000000000)
    ), 
     '0x0000000000000000000000000000000000000000', ((0x00, 1, '0x0000000000000000000000000000000000000000'),), (), (('0xD2f4D892fb7615989A73667aA8B477a2BFCfa6C9', 10000),), 0x0000)
