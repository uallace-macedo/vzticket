package server

import (
	"os"
	"time"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
	"github.com/redis/go-redis/v9"
	"github.com/uallace-macedo/livebit/livebit-bidder/internal/infra/auth"
	"github.com/uallace-macedo/livebit/livebit-bidder/internal/infra/config"
	"github.com/uallace-macedo/livebit/livebit-bidder/internal/infra/logger"
)

type server struct {
	config    *config.Config
	logger    *logger.Logger
	container *Container
}

func New(config *config.Config, logger *logger.Logger, redis *redis.Client) *server {
	return &server{
		config:    config,
		logger:    logger,
		container: NewContainer(config, logger, redis),
	}
}

func (s *server) Start() {
	server := gin.New()

	server.Use(cors.New(cors.Config{
		AllowOrigins:     []string{s.config.ApplicationConfig.Client.Url},
		AllowMethods:     []string{"GET", "POST", "PUT", "DELETE", "OPTIONS"},
		AllowHeaders:     []string{"Origin", "Content-Type", "Authorization", "Accept", "X-Requested-With"},
		AllowCredentials: true,
		MaxAge:           12 * time.Hour,
	}))

	s.setupMiddlewares(server)
	s.container.registerRoutes(server)
	server.Run(":" + s.config.ApplicationConfig.API.Port)
}

func (s *server) setupMiddlewares(server *gin.Engine) {
	publicKey, err := os.ReadFile("certs/publicKey.pem")
	if err != nil {
		s.logger.FatalErrorf("could not read public key: %v", err)
	}

	tokenValidator := auth.NewTokenValidator(s.logger, publicKey)
	server.Use(auth.NewMiddleware(s.config.ApplicationConfig.API.JwtCookieName, tokenValidator).Authenticate())
}
