package com.uallace.livebit.bid;

import com.uallace.livebit.auction.AuctionEntity;
import com.uallace.livebit.auction.AuctionRepository;
import com.uallace.livebit.auction.exceptions.AuctionNotFoundException;
import com.uallace.livebit.bid.dto.BidPlacedEvent;
import com.uallace.livebit.bid.exceptions.InvalidBidAmount;
import com.uallace.livebit.user.UserEntity;
import com.uallace.livebit.user.UserRepository;
import com.uallace.livebit.user.exceptions.UserNotFoundException;
import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.time.OffsetDateTime;

@Slf4j
@Service
@RequiredArgsConstructor
public class BidService {
    private final BidRepository bidRepository;
    private final AuctionRepository auctionRepository;
    private final UserRepository userRepository;
    private final StringRedisTemplate redisTemplate;

    @Transactional
    @KafkaListener(topics = "${KAFKA_BID_TOPIC}", groupId = "${spring.kafka.consumer.group-id}")
    public void consume(BidPlacedEvent event) {
        try {
            AuctionEntity auction = auctionRepository.findById(event.auctionID())
                    .orElseThrow(() -> new AuctionNotFoundException("Auction with ID: " + event.auctionID().toString() + " not found"));

            UserEntity user = userRepository.findById(event.userID())
                            .orElseThrow(() -> new UserNotFoundException("User with ID: " + event.userID().toString() + " not found"));


            if(auction.getCurrentPrice().compareTo(event.amount()) >= 0) {
                throw new InvalidBidAmount("Bid amount gotta be higher than: " + auction.getCurrentPrice());
            }

            updateAuctionCurrentPrice(auction, event.amount());
            saveBid(auction, user, event);

            auctionRepository.flush();
            bidRepository.flush();

            setupRedisValues(event);
        } catch (Exception e) {
            //
        }
    }

    private void updateAuctionCurrentPrice(AuctionEntity auctionEntity, BigDecimal value) {
        auctionEntity.setCurrentPrice(value);
    }

    private void saveBid(AuctionEntity auction, UserEntity user, BidPlacedEvent event) {
        BidEntity bid = new BidEntity();
        bid.setAuction(auction);
        bid.setBidder(user);
        bid.setAmount(event.amount());
        bid.setCreatedAt(OffsetDateTime.now());
        bidRepository.save(bid);
    }

    private void setupRedisValues(BidPlacedEvent event) {
        String key = "auction::" + event.auctionID();
        String value = event.amount().toString();

        try {
            redisTemplate.opsForValue().set(key, value);
            log.info("Redis updated for {} current price: {}", key, value);
        } catch (Exception e) {
            log.error("Could not update auctions price: {}", event.auctionID(), e);
        }
    }
}
