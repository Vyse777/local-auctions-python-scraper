import sqlite3
from datetime import datetime, timezone
from models.auction_models import Auction, AuctionItem
from utilities.config import DB_PATH


def init_db():
    print("Initializing database")
    conn = sqlite3.connect(DB_PATH, timeout=60.0)
    c = conn.cursor()
    c.executescript(
        """
        CREATE TABLE IF NOT EXISTS auctions (
            id TEXT PRIMARY KEY,
            name TEXT,
            url TEXT,
            address TEXT,
            city TEXT,
            state TEXT,
            zip TEXT,
            start_date_time TEXT,
            end_date_time TEXT,
            last_updated_at TEXT
        );

        CREATE TABLE IF NOT EXISTS auction_items (
            id TEXT PRIMARY KEY,
            auction_id TEXT,
            name TEXT,
            url TEXT,
            description TEXT,
            lot_number TEXT,
            last_updated_at TEXT,
            FOREIGN KEY(auction_id) REFERENCES auctions(id)
        );

        CREATE TABLE IF NOT EXISTS auction_item_images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            auction_item_id TEXT,
            url TEXT,
            last_updated_at TEXT,
            FOREIGN KEY(auction_item_id) REFERENCES auction_items(id)
        );
    """
    )
    conn.commit()
    conn.close()
    print("Database initialization complete")


def save_auction_to_db(auction: Auction):
    conn = sqlite3.connect(DB_PATH, timeout=60.0)
    c = conn.cursor()
    c.execute(
        """
        INSERT OR REPLACE INTO auctions (
        id,
        name,
        url,
        address,
        city,
        state,
        zip,
        start_date_time,
        end_date_time,
        last_updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """,
        (
            auction.id,
            auction.name,
            auction.url,
            auction.address,
            auction.city,
            auction.state,
            auction.zip,
            auction.start_date_time,
            auction.end_date_time,
            datetime.now(timezone.utc).isoformat(),
        ),
    )
    conn.commit()
    conn.close()


def save_items_to_db(items: list[AuctionItem]):
    conn = sqlite3.connect(DB_PATH, timeout=60.0)
    c = conn.cursor()
    updated_at = datetime.now(timezone.utc).isoformat()
    c.executemany(
        """
        INSERT OR REPLACE INTO auction_items (
            id,
            auction_id,
            name,
            url,
            description,
            lot_number,
            last_updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
        [
            (
                item.id,
                item.auction_id,
                item.name,
                item.url,
                item.description,
                item.lot_number,
                updated_at,
            )
            for item in items
        ],
    )
    c.executemany(
        """
        INSERT OR REPLACE INTO auction_item_images (
            auction_item_id,
            url,
            last_updated_at)
        VALUES (?, ?, ?)
    """,
        [
            (item.id, image_url, updated_at)
            for item in items
            for image_url in getattr(item, "image_urls", [])
        ],
    )
    conn.commit()
    conn.close()
