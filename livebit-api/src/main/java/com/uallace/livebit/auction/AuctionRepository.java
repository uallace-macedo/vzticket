package com.uallace.livebit.auction;

import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Slice;
import org.springframework.data.jpa.repository.JpaRepository;

import java.time.OffsetDateTime;
import java.util.UUID;

public interface AuctionRepository extends JpaRepository<AuctionEntity, UUID> {
    Slice<AuctionEntity> findByEndsAtAfter(OffsetDateTime date, PageRequest pageRequest);
}
