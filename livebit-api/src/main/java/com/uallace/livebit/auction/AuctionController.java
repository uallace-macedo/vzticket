package com.uallace.livebit.auction;

import com.uallace.livebit.auction.dto.CreateInput;
import com.uallace.livebit.auction.dto.CreateOutput;
import com.uallace.livebit.user.UserEntity;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.oauth2.jwt.Jwt;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.UUID;

@RestController
@RequestMapping("/api/v1/auctions")
@RequiredArgsConstructor
public class AuctionController {
    private final AuctionService auctionService;

    @PostMapping("")
    public ResponseEntity<CreateOutput> create(@RequestBody @Valid CreateInput input, @AuthenticationPrincipal Jwt jwt) {
        UUID userID = UUID.fromString(jwt.getSubject());
        CreateOutput body = auctionService.create(input, userID);
        return ResponseEntity.status(HttpStatus.CREATED).body(body);
    }
}
