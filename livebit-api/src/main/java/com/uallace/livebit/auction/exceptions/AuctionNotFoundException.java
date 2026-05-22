package com.uallace.livebit.auction.exceptions;

import lombok.extern.slf4j.Slf4j;

@Slf4j
public class AuctionNotFoundException extends RuntimeException {
    public AuctionNotFoundException(String message) {
        super(message);
        log.error(message);
    }
}
