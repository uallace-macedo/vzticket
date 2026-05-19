package com.uallace.livebit.auction;

import com.uallace.livebit.auction.dto.CreateInput;
import com.uallace.livebit.auction.dto.CreateOutput;
import com.uallace.livebit.auction.exceptions.InvalidEndsAtException;
import com.uallace.livebit.user.UserEntity;
import com.uallace.livebit.user.UserRepository;
import com.uallace.livebit.user.exceptions.UserNotFoundException;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Slice;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;

import java.time.OffsetDateTime;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class AuctionService {
    private final UserRepository userRepository;
    private final AuctionRepository auctionRepository;

    public CreateOutput create(CreateInput input, UUID ownerID) {
        if(input.endsAt().isBefore(input.startsAt())) throw new InvalidEndsAtException(input.startsAt());
        UserEntity user = userRepository.findById(ownerID).orElseThrow(() -> new UserNotFoundException(ownerID));

        AuctionEntity auction = new AuctionEntity();
        auction.setTitle(input.title());
        auction.setDescription(input.description());
        auction.setStartingPrice(input.startingPrice());
        auction.setStartsAt(input.startsAt());
        auction.setEndsAt(input.endsAt());
        auction.setOwner(user);

        AuctionEntity created = auctionRepository.save(auction);
        return new CreateOutput(
                created.getId(),
                created.getTitle(),
                created.getDescription(),
                created.getStartingPrice(),
                created.getStartsAt(),
                created.getEndsAt(),
                ownerID
        );
    }
}
