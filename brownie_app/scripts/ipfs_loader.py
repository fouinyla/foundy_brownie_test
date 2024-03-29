import json
import os

import requests
from brownie import config
from scripts.helpful_scripts import get_file_path


class IPFSLoader:
    """
    A class to interact with an IPFS node for pinning files and JSON data. It handles
    uploading and pinning of content on IPFS using a specified API.

    Attributes:
        FILES_DIRECTORY (str): The default directory for files to be pinned.
        API_BASE_URL (str): The base URL for the IPFS API.
        GATEWAY_URL (str): The IPFS gateway URL for accessing the pinned content.
    """

    FILES_DIRECTORY: str = os.getenv('FILES_DIRECTORY')
    API_BASE_URL: str = config['ipfs'].get('api_url')
    GATEWAY_URL: str = config['ipfs'].get('gateway_url', 'https://ipfs.io/ipfs')
    def __init__(self):
        self.headers = {
            'accept': 'application/json',
            'authorization': f'Bearer {config["ipfs"].get("api_key")}'
        }

    def pin_file(self, file_path) -> dict:
        """
        Pins the file to IPFS by sending a POST request to the IPFS API endpoint.

        Args:
            file_path (str): The file path of the content to be pinned.

        Returns:
            dict: The response from the IPFS API as a JSON object, typically containing the IPFS hash.
        """
        method: str = 'pinning/pinFileToIPFS'
        with open(file_path, "rb") as data:
            file_data = data.read()
        response = requests.post(f'{self.API_BASE_URL}/{method}', files={'file': file_data}, headers=self.headers)
        response_json = response.json()
        return response_json

    def pin_json(self, string: str) -> dict:
        """
        Pins JSON data to IPFS by sending it as a POST request to the IPFS API endpoint.

        Args:
            string (str): A string representation of the JSON data to be pinned.

        Returns:
            dict: The response from the IPFS API as a JSON object, typically containing the IPFS hash.
        """
        method: str = 'pinning/pinJSONToIPFS'
        payload = { "pinataContent": string}
        self.headers["content-type"] = "application/json"
        response = requests.post((f'{self.API_BASE_URL}/{method}'), json=payload, headers=self.headers)
        response_json = response.json()
        return response_json

    def get_uploadet_metadata_link(self, image_path: str, image_name: str) -> str:
        """
        Pins an image and its metadata JSON to IPFS, and constructs the metadata URL.

        This method takes the path to an image, pins it to IPFS, constructs a metadata JSON object
        with a link to the image, pins this metadata, and returns the link to the pinned metadata.

        Args:
            image_path (str): The file path of the image to be pinned.
            image_name (str): The name of the image to be included in the metadata.

        Returns:
            str: The URL to the pinned metadata on the IPFS gateway.
        """
        image_cid: str = self.pin_file(file_path=image_path)['IpfsHash']

        metadata: dict = {
            'name': 'DINDEX',
            'description': 'Dynamic Index NFT',
            'image': f'{self.GATEWAY_URL}/{image_cid}?filename={image_name}'
        }
        metadata_file_name: str = 'metadata.json'
        metadata_file_path: str = get_file_path(metadata_file_name)

        with open(metadata_file_path, 'w', encoding='utf8') as file_:
            metadata_json = json.dumps(metadata)
            file_.write(metadata_json)

        metadata_cid: str = self.pin_file(file_path=metadata_file_path)['IpfsHash']
        return f'{self.GATEWAY_URL}/{metadata_cid}?filename={metadata_file_name}'