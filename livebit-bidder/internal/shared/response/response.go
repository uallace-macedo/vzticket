package response

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

type (
	Response struct {
		Data  any        `json:"data,omitempty"`
		Error *ErrorBody `json:"error,omitempty"`
	}

	ErrorBody struct {
		Code    string       `json:"code"`
		Message string       `json:"message"`
		Details []FieldError `json:"details"`
	}

	FieldError struct {
		Field   string `json:"field"`
		Message string `json:"message"`
	}
)

func OK(c *gin.Context, data any) {
	c.JSON(http.StatusOK, data)
}

func BadRequest(c *gin.Context, err error) {
	c.JSON(http.StatusBadRequest, Response{Error: &ErrorBody{
		Code:    "bad_request",
		Message: err.Error(),
	}})
}

func InternalServerError(c *gin.Context, err error) {
	c.JSON(http.StatusInternalServerError, Response{Error: &ErrorBody{
		Code:    "internal_server_error",
		Message: err.Error(),
	}})
}

func ValidationError(c *gin.Context, errs []FieldError) {
	c.JSON(http.StatusBadRequest, Response{Error: &ErrorBody{
		Code:    "validation_error",
		Message: "invalid request",
		Details: errs,
	}})
}
