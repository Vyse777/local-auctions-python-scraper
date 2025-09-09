class AuctionItem:

    def __init__(
        self,
        id,
        auction_id,
        name,
        url,
        description,
        lot_number,
        image_urls: list[str],
    ):
        self.id = id
        self.auction_id = auction_id
        self.name = name
        self.url = url
        self.description = description
        self.lot_number = lot_number
        self.image_urls = image_urls


class Auction:
    def __init__(
        self, id, name, url, address, city, state, zip, start_date_time, end_date_time
    ):
        self.id = id
        self.name = name
        self.url = url
        # TODO: Abstract address into value object
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.start_date_time = start_date_time
        self.end_date_time = end_date_time
