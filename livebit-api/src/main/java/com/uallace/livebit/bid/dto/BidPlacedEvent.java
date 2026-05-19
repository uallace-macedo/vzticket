package com.uallace.livebit.bid.dto;

import com.fasterxml.jackson.databind.PropertyNamingStrategies;
import com.fasterxml.jackson.databind.annotation.JsonNaming;

import java.math.BigDecimal;
import java.util.UUID;

@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
public record BidPlacedEvent(
        UUID auctionID,
        UUID userID,
        BigDecimal amount
) {}
