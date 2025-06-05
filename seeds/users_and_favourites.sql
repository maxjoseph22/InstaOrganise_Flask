CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    auth0_id VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE,
    username VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE favourite_dogs (
    id SERIAL PRIMARY KEY,
    user_id int not null,
    constraint fk_user foreign key(user_id)
    references users(id)
    on delete cascade,
    dog_id INT NOT NULL,
    constraint fk_dog foreign key(dog_id)
    references dogs(id)
    on delete cascade,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE connections (
    id SERIAL PRIMARY KEY,
    user_id_1 INT NOT NULL,
    user_id_2 INT NOT NULL,        
    created_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (user_id_1) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id_2) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT unique_connection UNIQUE (user_id_1, user_id_2)
);
