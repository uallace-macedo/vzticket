package config

type (
	API struct {
		Port string
	}

	Client struct {
		Url string
	}

	ApplicationConfig struct {
		API    *API
		Client *Client
	}
)

func GetApplicationConfig() *ApplicationConfig {
	return &ApplicationConfig{
		API: &API{
			Port: getEnv("GOLANG_API_PORT", "5001"),
		},

		Client: &Client{
			Url: getEnv("CLIENT_URL", "http://localhost:5002"),
		},
	}
}
