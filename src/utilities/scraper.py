from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


def get_main_phoenix_auctions(main_auctions_url: str) -> set[str]:
    print(
        "Fetching auction information using Playwright. This might take some time... And RAM..."
    )
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(main_auctions_url)
        content = page.content()
        browser.close()

    print("Done. Parsing response and extracting auction links")
    auction_links = set()
    for a in BeautifulSoup(content, "html.parser").select(
        'a[title="Enter This Auction"][href*="/auction/"]'
    ):
        href = a.get("href")
        # Strip the '/bidgallery/' suffix - save some bits. If you open a link without it, it get's added back if it's needed
        if href.endswith("/bidgallery/"):
            href = href[0:-12]
        auction_links.add(href)

    print(f"Found {len(auction_links)} links")
    return auction_links
