package main

import (
	"github.com/uallace-macedo/livebit/livebit-bidder/internal/infra/config"
	"github.com/uallace-macedo/livebit/livebit-bidder/internal/infra/database"
	"github.com/uallace-macedo/livebit/livebit-bidder/internal/infra/logger"
	"github.com/uallace-macedo/livebit/livebit-bidder/internal/infra/server"
)

func main() {
	config := config.New()
	logger := logger.New("")
	redis := database.ConnectRedis(config.DataConfig.Redis, logger)

	server.New(config, logger, redis).Start()
}
