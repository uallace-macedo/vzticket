package auth

import (
	"fmt"
	"strings"

	"github.com/golang-jwt/jwt/v5"
	"github.com/uallace-macedo/livebit/livebit-bidder/internal/infra/logger"
)

type Claims struct {
	Scope string `json:"scp"`
	Email string `json:"email"`
	jwt.RegisteredClaims
}

type TokenValidator struct {
	logger    *logger.Logger
	publicKey []byte
}

func NewTokenValidator(logger *logger.Logger, pubKey []byte) *TokenValidator {
	return &TokenValidator{logger: logger, publicKey: pubKey}
}

func (v *TokenValidator) Validate(tokenString string) error {
	if strings.TrimSpace(tokenString) == "" {
		return jwt.ErrTokenUnverifiable
	}

	publicKey, err := jwt.ParseRSAPublicKeyFromPEM(v.publicKey)
	if err != nil {
		v.logger.Errorf("could not read public key: %v", err)
		return fmt.Errorf("could not read public key: %v", err)
	}

	token, err := jwt.ParseWithClaims(tokenString, &Claims{}, func(t *jwt.Token) (any, error) {
		if _, ok := t.Method.(*jwt.SigningMethodRSA); !ok {
			return nil, fmt.Errorf("invalid signature method: %v", t.Header["alg"])
		}
		return publicKey, nil
	})

	if err != nil {
		return fmt.Errorf("invalid or expired token")
	}

	if _, ok := token.Claims.(*Claims); ok {
		return nil
	}

	return fmt.Errorf("invalid token")
}
