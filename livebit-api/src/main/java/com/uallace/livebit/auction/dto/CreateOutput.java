package com.uallace.livebit.auction.dto;

import java.math.BigDecimal;
import java.time.OffsetDateTime;
import java.util.UUID;

public record CreateOutput(
        UUID id,
        String title,
        String description,
        BigDecimal startingPrice,
        OffsetDateTime startsAt,
        OffsetDateTime endsAt,
        UUID ownerID
) {}
