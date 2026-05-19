package com.uallace.livebit.auction;

import com.uallace.livebit.bid.BidEntity;
import com.uallace.livebit.user.UserEntity;
import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

import java.math.BigDecimal;
import java.time.OffsetDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

@Table(name = "auctions")
@Entity
@Getter
@Setter
public class AuctionEntity {
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column(nullable = false)
    private String title;
    private String description;

    @Column(name = "starting_price", nullable = false, updatable = false)
    private BigDecimal startingPrice;

    @Column(name = "current_price", nullable = false)
    private BigDecimal currentPrice = new BigDecimal(0);

    @Column(nullable = false)
    @Enumerated(EnumType.STRING)
    private AuctionStatus status = AuctionStatus.SCHEDULED;

    @Column(name = "starts_at", nullable = false)
    private OffsetDateTime startsAt;

    @Column(name = "ends_at", nullable = false)
    private OffsetDateTime endsAt;

    @ManyToOne
    @JoinColumn(name = "owner_id")
    private UserEntity owner;

    @ManyToOne
    @JoinColumn(name = "winner_id")
    private UserEntity winner;

    @OneToMany(mappedBy = "auction")
    List<BidEntity> bids = new ArrayList<>();
}
