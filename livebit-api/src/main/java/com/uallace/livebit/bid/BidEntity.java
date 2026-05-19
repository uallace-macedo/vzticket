package com.uallace.livebit.bid;

import com.uallace.livebit.auction.AuctionEntity;
import com.uallace.livebit.user.UserEntity;
import jakarta.persistence.*;

import java.math.BigDecimal;
import java.time.OffsetDateTime;
import java.util.UUID;

@Table(name = "bids")
@Entity
public class BidEntity {
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column(nullable = false)
    @ManyToOne
    @JoinColumn(name = "auction_id")
    private AuctionEntity auction;

    @Column(nullable = false)
    @ManyToOne
    @JoinColumn(name = "bidder_id")
    private UserEntity bidder;

    @Column(nullable = false)
    private BigDecimal amount;

    @Column(name = "created_at", nullable = false, updatable = false)
    private OffsetDateTime createdAt;
}
