from ..collection import Collection
from ..nft import NFT
import requests
import logging


class Solanart (Collection):

    def __init__(self, name):
        url = 'https://qzlsklfacc.medianetwork.cloud/query_volume_all'
        collections = requests.get(url).json()
        for coll in collections:
            if coll.get('collection') == name:
                floor_price = coll.get('floorPrice')
                super().__init__(name, floor_price)

    def _get_nfts(self):
        ''' Get list of NFTs for sale by a collection '''
        url = f'https://qzlsklfacc.medianetwork.cloud/nft_for_sale?collection={self.name}'
        try:
            return requests.get(url).json()
        except Exception as e:
            logging.error(e)
            return []

    def _to_nft(self, raw_nft):
        ''' Format raw NFT data to nft object '''
        name = raw_nft.get('name')
        price = raw_nft.get('price')
        for_sale = bool(raw_nft.get('for_sale'))

        if for_sale:
            return NFT(name, price)
