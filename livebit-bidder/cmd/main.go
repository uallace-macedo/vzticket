package main

import (
	"reflect"
	"strings"

	"github.com/gin-gonic/gin/binding"
	"github.com/go-playground/validator/v10"
	"github.com/uallace-macedo/livebit/livebit-bidder/internal/infra/config"
	"github.com/uallace-macedo/livebit/livebit-bidder/internal/infra/database"
	"github.com/uallace-macedo/livebit/livebit-bidder/internal/infra/logger"
	"github.com/uallace-macedo/livebit/livebit-bidder/internal/infra/server"
)

func main() {
	config := config.New()
	logger := logger.New("")
	redis := database.ConnectRedis(config.DataConfig.Redis, logger)

	configValidationErrors()
	server.New(config, logger, redis).Start()
}

func configValidationErrors() {
	if v, ok := binding.Validator.Engine().(*validator.Validate); ok {
		v.RegisterTagNameFunc(func(fld reflect.StructField) string {
			name := strings.SplitN(fld.Tag.Get("json"), ",", 2)[0]
			if name == "-" {
				return ""
			}
			return name
		})
	}
}
