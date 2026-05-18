package org.uallace.livebit.auction;

import jakarta.persistence.*;
import org.uallace.livebit.user.UserEntity;

import java.math.BigDecimal;
import java.time.OffsetDateTime;
import java.util.UUID;

@Table(name = "auctions")
@Entity
public class AuctionEntity {
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    public UUID id;

    @Column(nullable = false)
    public String title;
    public String description;

    @Column(name = "starting_price", nullable = false)
    public BigDecimal startingPrice;

    @Column(name = "current_price", nullable = false)
    public BigDecimal currentPrice;

    @Column(nullable = false)
    @Enumerated(EnumType.STRING)
    public AuctionStatus status;

    @Column(name = "starts_at", nullable = false)
    public OffsetDateTime startsAt;

    @Column(name = "ends_at", nullable = false)
    public OffsetDateTime endsAt;

    @ManyToOne
    @JoinColumn(name = "owner_id")
    public UserEntity owner;

    @ManyToOne
    @JoinColumn(name = "winner_id")
    public UserEntity winner;
}
