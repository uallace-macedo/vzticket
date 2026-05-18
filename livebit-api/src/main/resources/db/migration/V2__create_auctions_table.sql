CREATE TABLE IF NOT EXISTS auctions (
    id UUID PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    starting_price NUMERIC(14, 2) NOT NULL DEFAULT 0,
    current_price NUMERIC(14, 2) NOT NULL DEFAULT 0,
    status VARCHAR(20) NOT NULL DEFAULT 'SCHEDULED',
    starts_at TIMESTAMPTZ NOT NULL,
    ends_at TIMESTAMPTZ NOT NULL,
    owner_id UUID NOT NULL,
    winner_id UUID,

    CONSTRAINT fk_auction_owner_id FOREIGN KEY (owner_id) REFERENCES users(id),
    CONSTRAINT fk_auction_winner_id FOREIGN KEY (winner_id) REFERENCES users(id)
);