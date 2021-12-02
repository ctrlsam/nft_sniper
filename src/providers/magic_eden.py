from ..collection import Collection
from ..nft import NFT
import requests
import logging


class MagicEden (Collection):

    def __init__(self, name):
        url = f'https://api-mainnet.magiceden.io/rpc/getCollectionEscrowStats/{name}'
        req = requests.get(url).json()
        floor_price = int(req.get('results').get('floorPrice')) / 1000000000
        super().__init__(name, floor_price)

    def _get_nfts(self):
        ''' Get list of NFTs for sale by a collection '''
        url = f'https://api-mainnet.magiceden.io/rpc/getListedNFTsByQuery?q={{"$match":{{"collectionSymbol":"{self.name}"}},"$sort":{{"blockTime":-1}} }}'
        try:
            return requests.get(url).json().get('results')
        except Exception as e:
            logging.error(e)
            return []

    def _to_nft(self, raw_nft):
        ''' Format raw NFT data to nft object '''
        mint_address = raw_nft.get('mintAddress')
        name = f'https://magiceden.io/item-details/{mint_address}'
        price = raw_nft.get('price')

        return NFT(name, price)
