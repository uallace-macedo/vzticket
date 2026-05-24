package config

type (
	Redis struct {
		Host     string
		Port     int
		Password string
	}

	DataConfig struct {
		Redis *Redis
	}
)

func GetDataConfig() *DataConfig {
	return &DataConfig{
		Redis: &Redis{
			Host:     getEnv("REDIS_HOST", "localhost"),
			Port:     getIntEnv("REDIS_PORT", 0),
			Password: getEnv("REDIS_PASSWORD", ""),
		},
	}
}
