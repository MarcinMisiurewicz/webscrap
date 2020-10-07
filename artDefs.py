class Piece:
    def __init__(self, name, artist, technique):
        self.name = name
        self.artist = artist
        self.technique = technique
        self.auctions = []

    def append_auctions(self, auction_date, price):
        self.auctions.append((auction_date, price))

