from brownie import config
from scripts.create_index_image import get_generated_index_image_name
from scripts.index_calculator import IndexCalculator
from scripts.ipfs_loader import IPFSLoader
from scripts.OpenAI import get_generated_image_name
from scripts.update_index import update_index


def main():

    # 1.Calculate index
    index_assets_config = [
        {'ticker': 'UNI', 'address': '0xb33EaAd8d922B1083446DC23f610c2567fB5180f', 'amount': None, 'price': None, 'total_price': None},
        {'ticker': '1INCH', 'address': '0x9c2C5fd7b07E95EE044DDeba0E97a665F142394f', 'amount': None, 'price': None, 'total_price': None},
        {'ticker': 'KNC', 'address': '0x1C954E8fe737F99f68Fa1CCda3e51ebDB291948C', 'amount': None, 'price': None, 'total_price': None}
    ]
    index_calculator = IndexCalculator(
        price_provider=config['price_provider'].get('url'),
        index_assets_config=index_assets_config,
        wnft_contract_address='0x347d5125a7b5b8c14400bfc8d8230014b9cd3033',
        wnft_id=7,
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
        dindex_contact_address='0x271c2Bf44283cC5770Fc5005bdDD3817609aAEF9',
        ipfs_metadata_link=ipfs_metadata_link,
        token_id=1
    )
    print(f'Update transaction: {update_transaction}')


