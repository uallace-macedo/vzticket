package org.uallace.livebit.user;

import io.quarkus.hibernate.orm.panache.PanacheEntityBase;
import jakarta.persistence.*;
import org.uallace.livebit.auction.AuctionEntity;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

@Entity
@Table(name = "users")
public class UserEntity extends PanacheEntityBase {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    public UUID id;

    @Column(nullable = false, unique = true)
    public String username;

    @Column(nullable = false, unique = true)
    public String email;

    @Column(nullable = false)
    public String password;

    @Column(nullable = false)
    @Enumerated(EnumType.STRING)
    public UserRole role;

    @Column(name = "created_at", nullable = false, updatable = false)
    public LocalDateTime createdAt;

    @OneToMany(mappedBy = "owner")
    public List<AuctionEntity> auctions = new ArrayList<>();

    @OneToMany(mappedBy = "winner")
    public List<AuctionEntity> wonAuctions = new ArrayList<>();

    @PrePersist
    public void prePersist() {
        createdAt = LocalDateTime.now();
    }
}
