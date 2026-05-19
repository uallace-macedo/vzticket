package com.uallace.livebit.auction;

import com.uallace.livebit.auction.dto.AuctionOutput;
import com.uallace.livebit.auction.dto.CreateInput;
import com.uallace.livebit.auction.dto.CreateOutput;
import com.uallace.livebit.user.UserEntity;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Slice;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.oauth2.jwt.Jwt;
import org.springframework.web.bind.annotation.*;

import java.util.UUID;

@RestController
@RequestMapping("/api/v1/auctions")
@RequiredArgsConstructor
public class AuctionController {
    private final AuctionService auctionService;

    @GetMapping("")
    public ResponseEntity<Slice<AuctionOutput>> getActiveAuctions(
            @RequestParam(value = "page", defaultValue = "0") int page,
            @RequestParam(value = "size", defaultValue = "10") int size
    ) {
        Slice<AuctionOutput> activeAuctions = auctionService.getActiveAuctions(page, size);
        return ResponseEntity.ok().body(activeAuctions);
    }

    @PostMapping("")
    public ResponseEntity<CreateOutput> create(@RequestBody @Valid CreateInput input, @AuthenticationPrincipal Jwt jwt) {
        UUID userID = UUID.fromString(jwt.getSubject());
        CreateOutput body = auctionService.create(input, userID);
        return ResponseEntity.status(HttpStatus.CREATED).body(body);
    }
}
