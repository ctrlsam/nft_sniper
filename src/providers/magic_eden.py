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
        url = f'https://api-mainnet.magiceden.io/rpc/getGlobalActivitiesByQuery?q={{"$match":{{"collection_symbol":"{self.name}"}},"$sort":{{"blockTime":-1}},"$skip":0}}'

        try:
            return requests.get(url).json().get('results')
        except Exception as e:
            logging.error(e)
            return []

    def _to_nft(self, raw_nft):
        ''' Format raw NFT data to nft object '''
        parsedList = raw_nft.get('parsedList')
        if not parsedList:
            return

        name = raw_nft.get('_id')  # use _id for now
        price = parsedList.get('amount') / 1000000000
        return NFT(name, price)
