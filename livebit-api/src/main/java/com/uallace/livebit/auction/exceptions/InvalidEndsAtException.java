package com.uallace.livebit.auction.exceptions;

import java.time.OffsetDateTime;

public class InvalidEndsAtException extends RuntimeException {
    public InvalidEndsAtException(OffsetDateTime createdAt) {
        super(String.format("End date must be after %s", createdAt.toString()));
    }
}
