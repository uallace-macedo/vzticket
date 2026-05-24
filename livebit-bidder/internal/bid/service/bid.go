package service

import (
	"context"
	"fmt"

	"github.com/redis/go-redis/v9"
	"github.com/shopspring/decimal"
)

func (s *service) Bid(ctx context.Context, authorID, auctionID string, amount decimal.Decimal) error {
	key := "auction::" + auctionID

	value, err := s.redis.Get(ctx, key).Result()
	if err == redis.Nil {
		return fmt.Errorf("auction [%s] not found", auctionID)
	}

	current, err := decimal.NewFromString(value)
	if err != nil {
		return fmt.Errorf("could not parse current value: %v", err)
	}

	if amount.LessThanOrEqual(current) {
		return fmt.Errorf("amount must be grather than %s", current.String())
	}

	s.logger.Infof("NEW AMOUNT GOTTA BE: %s", current.String())
	return nil
}
