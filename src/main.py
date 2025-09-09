import time
from utilities.api import get_auction_details_from_api, get_auction_items_from_api
from utilities.db import init_db, save_auction_to_db, save_items_to_db
from multiprocessing import Pool, cpu_count
from utilities.scraper import get_main_phoenix_auctions

from utilities.config import BASE_URL, USE_MULTIPROCESSING


# This function can be called with multiprocessing or sequentially
def fetch_and_store_auction_items(auction_url: str) -> int:
    # Extract the auction_id from the URL
    # Example URL: https://online.localauctions.com/auction/17434/bidgallery/
    auction_id = auction_url.split("/")[4]
    auction = get_auction_details_from_api(auction_id, auction_url)
    save_auction_to_db(auction)
    auction_items = get_auction_items_from_api(auction)
    save_items_to_db(auction_items)
    return len(auction_items)


def main():
    init_db()
    auction_links = get_main_phoenix_auctions(BASE_URL)

    if USE_MULTIPROCESSING:
        print(
            f"Multiprocessing enabled. Will create a pool with size: {min(cpu_count(), len(auction_links))}"
        )
        with Pool(min(cpu_count(), len(auction_links))) as pool:
            results = pool.map(fetch_and_store_auction_items, auction_links)
        print(
            f"Finished multiprocessing {len(auction_links)} auctions. Found a total of {sum(results)} auction items"
        )
    else:
        print(
            f"Multiprocessing disabled. Will sequentially fetch and store {len(auction_links)} auctions"
        )
        for link in auction_links:
            fetch_and_store_auction_items(link)


if __name__ == "__main__":
    start = time.time()
    print("Starting application")
    main()
    print(f"Application completed in {time.time() - start:.2f} seconds.")
