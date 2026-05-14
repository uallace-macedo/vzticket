package config

import (
	"os"
	"strconv"
)

func getEnv(k, fb string) string {
	if v, ok := os.LookupEnv(k); ok {
		return v
	}

	return fb
}

func getIntEnv(k string, fb int) int {
	if v, ok := os.LookupEnv(k); ok {
		if i, err := strconv.Atoi(v); err == nil {
			return i
		}
	}

	return fb
}
