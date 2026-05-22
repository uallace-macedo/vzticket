package com.uallace.livebit.infra.kafka;

import com.uallace.livebit.bid.exceptions.InvalidBidAmount;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.listener.DefaultErrorHandler;
import org.springframework.util.backoff.FixedBackOff;

@Configuration
public class KafkaConfig {
    @Bean
    public DefaultErrorHandler errorHandler() {
        DefaultErrorHandler errorHandler = new DefaultErrorHandler(new FixedBackOff(1000L, 2));
        errorHandler.addNotRetryableExceptions(InvalidBidAmount.class);
        return errorHandler;
    }
}
