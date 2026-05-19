CREATE TABLE IF NOT EXISTS bids (
    id UUID PRIMARY KEY gen_random_uuid(),
    auction_id UUID NOT NULL,
    bidder_id UUID NOT NULL,
    amount NUMERIC(14, 2) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_bids_auction_id FOREIGN KEY (auction_id) REFERENCES auctions(id),
    CONSTRAINT fk_bids_bidder_id FOREIGN KEY (bidder_id) REFERENCES users(id)
);