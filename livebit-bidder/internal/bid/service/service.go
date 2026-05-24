package service

import (
	"context"

	"github.com/redis/go-redis/v9"
	"github.com/shopspring/decimal"
	"github.com/uallace-macedo/livebit/livebit-bidder/internal/infra/logger"
)

type (
	Service interface {
		Bid(ctx context.Context, authorID, auctionID string, amount decimal.Decimal) error
	}

	service struct {
		logger *logger.Logger
		redis  *redis.Client
	}
)

func New(logger *logger.Logger, redis *redis.Client) *service {
	return &service{
		logger: logger,
		redis:  redis,
	}
}
