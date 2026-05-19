package com.uallace.livebit.auction.dto;

import com.fasterxml.jackson.databind.PropertyNamingStrategies;
import com.fasterxml.jackson.databind.annotation.JsonNaming;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import org.hibernate.validator.constraints.Length;

import java.math.BigDecimal;
import java.time.OffsetDateTime;

@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
public record CreateInput(
        @NotBlank @Length(min = 4, message = "Title must contain at least 4 chars") String title,
        String description,
        @NotNull BigDecimal startingPrice,
        @NotNull OffsetDateTime startsAt,
        @NotNull OffsetDateTime endsAt
) {}
