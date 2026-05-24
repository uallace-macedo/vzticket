package dto

import "github.com/shopspring/decimal"

type BidRequest struct {
	AuthorID  string           `json:"author_id" binding:"required"`
	AuctionID string           `json:"auction_id" binding:"required"`
	Amount    *decimal.Decimal `json:"amount" binding:"required"`
}
