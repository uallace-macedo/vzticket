package handler

import (
	"github.com/gin-gonic/gin"
	"github.com/redis/go-redis/v9"
	bidService "github.com/uallace-macedo/livebit/livebit-bidder/internal/bid/service"
	"github.com/uallace-macedo/livebit/livebit-bidder/internal/infra/logger"
)

type (
	Handler interface {
		bid(c *gin.Context)
	}

	handler struct {
		logger  *logger.Logger
		service bidService.Service
	}
)

func New(logger *logger.Logger, redis *redis.Client) *handler {
	bidService := bidService.New(logger, redis)

	return &handler{
		logger:  logger,
		service: bidService,
	}
}

func (h *handler) RegisterRoutes(r *gin.Engine) {
	group := r.Group("/api/v1/bids")
	group.POST("", h.bid)
}
