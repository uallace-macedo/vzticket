package auth

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

type Middleware struct {
	cookieName string
	validator  *TokenValidator
}

func NewMiddleware(cookieName string, validator *TokenValidator) *Middleware {
	return &Middleware{cookieName: cookieName, validator: validator}
}

func (m *Middleware) Authenticate() gin.HandlerFunc {
	return func(c *gin.Context) {
		tokenStr, err := c.Cookie(m.cookieName)
		if err != nil {
			c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"error": "authentication cookie not found"})
			return
		}

		err = m.validator.Validate(tokenStr)
		if err != nil {
			c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"error": "invalid token"})
			return
		}

		c.Next()
	}
}
