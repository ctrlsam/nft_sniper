class NFT:
    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.profit = 0

    def update_profit(self, profit):
        self.profit = profit
