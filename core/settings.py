from os import getenv

from dotenv import load_dotenv


load_dotenv()


class AppSettings:
    AUTHENTICATION_KEY: str = getenv("WEB_SERVER_AUTHENTICATION_KEY")
    STATIC_DIRECTORY: str = getenv("STATIC_DIRECTORY")


appSettings = AppSettings()


class WalletSettings:
    PRIVATE_KEY: str = getenv("WALLET_PRIVATE_KEY")


walletSettings = WalletSettings()


class InfuraSettings:
    PROJECT_ID: str = getenv("WEB3_INFURA_PROJECT_ID")


infuraSettings = InfuraSettings()


class PolygonSettings:
    PROD_RPC: str = getenv("POLYGON_PROD_RPC")
    MUMBAI_RPC: str = getenv("POLYGON_MUMBAI_RPC")


polygonSettings = PolygonSettings()


class CoinMarketCupSettings:
    API_KEY: str = getenv("CM_API_KEY")
    URL: str = getenv("CM_URL")


coinMarketCupSettings = CoinMarketCupSettings()


class PinataSettings:
    API_URL: str = getenv("PINATA_IPFS_API_URL")
    GATEWAY_URL: str = getenv("PINATA_GATEWAY_URL")
    TOKEN: str = getenv("PINATA_IPFS_TOKEN")


pinataSettings = PinataSettings()
