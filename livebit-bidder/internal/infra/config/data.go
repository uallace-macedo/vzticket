package config

type (
	Redis struct {
		Url      string
		Password string
	}

	DataConfig struct {
		Redis *Redis
	}
)

func GetDataConfig() *DataConfig {
	return &DataConfig{
		Redis: &Redis{
			Url:      getEnv("REDIS_HOST", ""),
			Password: getEnv("REDIS_PASSWORD", ""),
		},
	}
}
