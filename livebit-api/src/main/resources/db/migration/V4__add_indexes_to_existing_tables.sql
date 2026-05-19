-- users
CREATE INDEX IF NOT EXISTS idx_user_email ON users(email);

-- auctions
CREATE INDEX IF NOT EXISTS idx_auctions_owner_id ON auctions(owner_id);
CREATE INDEX IF NOT EXISTS idx_auctions_winner_id ON auctions(winner_id);

-- bids
CREATE INDEX IF NOT EXISTS idx_bids_auction_id ON bids(auction_id);
CREATE INDEX IF NOT EXISTS idx_bids_bidder_id ON bids(bidder_id);