package handler

import (
	"github.com/gin-gonic/gin"
	"github.com/uallace-macedo/livebit/livebit-bidder/internal/bid/handler/dto"
	"github.com/uallace-macedo/livebit/livebit-bidder/internal/shared/response"
)

func (h *handler) bid(c *gin.Context) {
	var req dto.BidRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		response.ValidationError(c, response.ParseValidationErrors(err))
		return
	}

	response.OK(c, response.Response{Data: req})
}
