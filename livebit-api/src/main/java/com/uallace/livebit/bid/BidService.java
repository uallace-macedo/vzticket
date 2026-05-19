package com.uallace.livebit.bid;

import com.uallace.livebit.bid.dto.BidPlacedEvent;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class BidService {
    private final BidRepository bidRepository;

    @KafkaListener(topics = "${KAFKA_BID_TOPIC}", groupId = "${spring.kafka.consumer.group-id}")
    public void consume(BidPlacedEvent event) {
        System.out.println(event);
    }
}
