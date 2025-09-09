import html
import json
import requests
import pycurl
from datetime import timezone
from dateutil import parser
from io import BytesIO
from models.auction_models import Auction, AuctionItem
from urllib.parse import urlencode


def get_auction_items_from_api(auction: Auction) -> list[AuctionItem]:
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, "https://online.localauctions.com/api/getitems")
    c.setopt(c.WRITEDATA, buffer)

    post_data = {
        "auction_id": auction.id,
        "item_type": "itemlist",
        "filters[perpage]": 5000,
    }
    postfields = urlencode(post_data)
    c.setopt(c.POSTFIELDS, postfields)
    c.perform()
    c.close()

    items_json = json.loads(buffer.getvalue().decode("utf-8"))["items"]
    print(f"Found {len(items_json)} items for auction_id {auction.id}")
    return list(
        map(
            lambda item: AuctionItem(
                id=item["id"],
                auction_id=item["auction_id"],
                name=html.unescape(item["title"]),
                url=item["item_url"].replace("\\", ""),
                description=item["description"],
                lot_number=item["lot_number"],
                image_urls=[image["image_url"] for image in item.get("images", [])],
            ),
            items_json,
        )
    )


def get_auction_details_from_api(auction_id: str, auction_url: str) -> Auction | None:
    print(f"Fetching auction metadata for auction {auction_id}")
    result = requests.get(f"https://online.localauctions.com/api/auctions/{auction_id}")
    auction_details = result.json()["data"]

    print(f"Auction metadata fetched for {auction_id}")
    return Auction(
        id=auction_details["id"],
        name=html.unescape(auction_details["title"]),
        url=auction_url,
        address=auction_details["address"],
        city=auction_details["city"],
        state=auction_details["state_abbreviation"],
        zip=auction_details["zip"],
        start_date_time=parser.parse(auction_details["starts"])
        .astimezone(timezone.utc)
        .isoformat(),
        end_date_time=parser.parse(auction_details["ends"])
        .astimezone(timezone.utc)
        .isoformat(),
    )
