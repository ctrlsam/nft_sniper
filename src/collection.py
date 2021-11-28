import logging


class Collection:

    def __init__(self, name, floor_price):
        self.name = name
        self.floor_price = floor_price
        self.nfts = None

    def get_opportunities(self, threshold=40):
        ''' Get NFT profitability '''
        self._update_nfts()  # update NFT prices

        for nft in self.nfts:
            profit = self._calculate_profit(nft.price)
            nft.update_profit(profit)

        for nft in self.nfts:
            logging.debug(
                f"nft with {nft.profit}% dosen't meet threshold of "
                f'{threshold}%')
            if nft.profit >= threshold:
                logging.success(f'nft found with {nft.profit}%'
                                f' below market value')
                yield nft

    def _calculate_profit(self, nft_price):
        ''' Calculates the difference in floor price and nft sale price '''
        return ((self.floor_price - nft_price) / self.floor_price) * 100

    def _get_nfts(self):
        ''' Get list of NFTS '''
        raise NotImplementedError

    def _to_nft(self):
        ''' Format raw NFT data to nft object '''
        raise NotImplementedError

    def _update_nfts(self):
        ''' Scan for NFTs and update list '''
        self.nfts = []
        for nft in self._get_nfts():
            nft_obj = self._to_nft(nft)
            if not nft_obj:
                continue
            self.nfts.append(nft_obj)
