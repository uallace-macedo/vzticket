package server

import (
	"github.com/gin-gonic/gin"
	"github.com/redis/go-redis/v9"
	bidHandler "github.com/uallace-macedo/livebit/livebit-bidder/internal/bid/handler"
	"github.com/uallace-macedo/livebit/livebit-bidder/internal/infra/config"
	"github.com/uallace-macedo/livebit/livebit-bidder/internal/infra/logger"
)

type Container struct {
	config *config.Config
	logger *logger.Logger
	redis  *redis.Client
}

func NewContainer(config *config.Config, logger *logger.Logger, redis *redis.Client) *Container {
	return &Container{
		config: config,
		logger: logger,
		redis:  redis,
	}
}

func (c *Container) registerRoutes(r *gin.Engine) {
	bidHandler.New(c.logger, c.redis).RegisterRoutes(r)
}
