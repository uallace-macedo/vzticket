CREATE EXTENSION "uuid-ossp";
CREATE TYPE USER_ROLE AS ENUM('user', 'admin');

CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(40) NOT NULL UNIQUE,
    email VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role USER_ROLE NOT NULL default 'user',
    created_at TIMESTAMP NOT NULL default current_timestamp
);
