package database

import (
	"context"
	"strconv"
	"time"

	"github.com/redis/go-redis/v9"
	"github.com/uallace-macedo/livebit/livebit-bidder/internal/infra/config"
	"github.com/uallace-macedo/livebit/livebit-bidder/internal/infra/logger"
)

type silentLogger struct{}

func (s silentLogger) Printf(ctx context.Context, format string, v ...any) {}

func ConnectRedis(redisConfig *config.Redis, log *logger.Logger) *redis.Client {
	addr := redisConfig.Host + ":" + strconv.Itoa(redisConfig.Port)
	redis.SetLogger(silentLogger{})

	opts := &redis.Options{
		Addr:        addr,
		Password:    redisConfig.Password,
		PoolSize:    10,
		ReadTimeout: 5 * time.Second,
		MaxRetries:  -1,
		DialTimeout: 1 * time.Second,
	}

	rdb := redis.NewClient(opts)
	ctx := context.Background()
	connected := false

	for range 5 {
		err := rdb.Ping(ctx).Err()
		if err == nil {
			connected = true
			break
		}

		log.Info("waiting redis to be ready...")
		time.Sleep(1 * time.Second)
	}

	if !connected {
		log.FatalError("could not connect to redis after 5 tries.")
	}

	log.Info("connected to redis successfully")
	return rdb
}
