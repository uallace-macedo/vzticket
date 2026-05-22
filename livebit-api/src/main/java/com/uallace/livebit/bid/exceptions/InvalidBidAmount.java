package com.uallace.livebit.bid.exceptions;

import lombok.extern.slf4j.Slf4j;

@Slf4j
public class InvalidBidAmount extends RuntimeException {
    public InvalidBidAmount(String message) {
        super(message);
        log.error(message);
    }
}
