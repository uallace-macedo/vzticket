package com.uallace.livebit.auction;

import com.uallace.livebit.auction.dto.AuctionOutput;

import java.time.OffsetDateTime;

public class AuctionMapper {
    public static AuctionOutput fromEntity(AuctionEntity entity) {
        if(entity == null) return null;

        AuctionOutput.MinimalUser ownerOutput = new AuctionOutput.MinimalUser(
                entity.getOwner().getId(),
                entity.getOwner().getName(),
                entity.getOwner().getEmail()
        );

        AuctionOutput.MinimalUser winnerOutput = entity.getWinner() != null ? new AuctionOutput.MinimalUser(
                entity.getWinner().getId(),
                entity.getWinner().getName(),
                entity.getWinner().getEmail()
        ) : null;

        boolean isOpen = OffsetDateTime.now().isBefore(entity.getEndsAt())
                && OffsetDateTime.now().isAfter(entity.getStartsAt());

        return new AuctionOutput(
                entity.getId(),
                entity.getTitle(),
                entity.getDescription(),
                entity.getStartingPrice(),
                entity.getCurrentPrice(),
                entity.getStartsAt(),
                entity.getEndsAt(),
                ownerOutput,
                winnerOutput,
                isOpen
        );
    }
}
