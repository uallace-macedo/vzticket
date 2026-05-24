package response

import (
	"errors"
	"fmt"
	"strings"

	"github.com/go-playground/validator/v10"
)

func ParseValidationErrors(err error) []FieldError {
	var ve validator.ValidationErrors
	if !errors.As(err, &ve) {
		return []FieldError{{Field: "request", Message: err.Error()}}
	}

	fields := make([]FieldError, len(ve))
	for i, fe := range ve {
		fields[i] = FieldError{
			Field:   strings.ToLower(fe.Field()),
			Message: validationMessage(fe),
		}
	}

	return fields
}

func validationMessage(fe validator.FieldError) string {
	switch fe.Tag() {
	case "required":
		return "This field is required"
	case "email":
		return "invalid email format"
	case "min":
		return fmt.Sprintf("minimum %s characters", fe.Param())
	case "max":
		return fmt.Sprintf("maximum %s characters", fe.Param())
	case "oneof":
		return fmt.Sprintf("must be one of %s", fe.Param())
	default:
		return "invalid value"
	}
}
