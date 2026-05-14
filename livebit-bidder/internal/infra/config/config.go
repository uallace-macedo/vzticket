package config

import "github.com/joho/godotenv"

func init() {
	godotenv.Load("../.env")
}

type Config struct {
	ApplicationConfig *ApplicationConfig
	DataConfig        *DataConfig
}

func New() *Config {
	return &Config{
		ApplicationConfig: GetApplicationConfig(),
		DataConfig:        GetDataConfig(),
	}
}
