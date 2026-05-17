package org.uallace.livebit.user;

import org.uallace.livebit.user.dto.UserDTO;

public class UserMapper {

    public static UserDTO toDto(UserEntity userEntity) {
        return new UserDTO(
            userEntity.id,
            userEntity.username,
            userEntity.email,
            userEntity.role
        );
    }
}
