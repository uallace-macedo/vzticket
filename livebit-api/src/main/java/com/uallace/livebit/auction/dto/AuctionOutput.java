package com.uallace.livebit.auction.dto;

import com.fasterxml.jackson.databind.PropertyNamingStrategies;
import com.fasterxml.jackson.databind.annotation.JsonNaming;

import java.math.BigDecimal;
import java.time.OffsetDateTime;
import java.util.UUID;

@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
public record AuctionOutput(
        UUID id,
        String title,
        String description,
        BigDecimal startingPrice,
        BigDecimal currentPrice,
        OffsetDateTime startsAt,
        OffsetDateTime endsAt,
        MinimalUser owner,
        MinimalUser winner,
        boolean isOpen
) {
    @JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
    public record MinimalUser(
            UUID id,
            String name,
            String email
    ) {}
}
