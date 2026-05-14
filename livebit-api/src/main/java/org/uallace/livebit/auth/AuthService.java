package org.uallace.livebit.auth;

import io.quarkus.elytron.security.common.BcryptUtil;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.transaction.Transactional;
import org.uallace.livebit.auth.exceptions.UserEmailAlreadyExistsException;
import org.uallace.livebit.user.UserEntity;

@ApplicationScoped
public class AuthService {
    @Transactional
    public UserEntity register(UserEntity userEntity) {
        if (UserEntity.find("email", userEntity.email).firstResult() != null) throw new UserEmailAlreadyExistsException();
        if (UserEntity.find("username", userEntity.username).firstResult() != null) throw new UserEmailAlreadyExistsException();

        userEntity.password = BcryptUtil.bcryptHash(userEntity.password);
        UserEntity.persist(userEntity);
        return userEntity;
    }
}
