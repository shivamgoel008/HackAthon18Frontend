create table users (
    username varchar(255) primary key,
    password varchar(255) not null,
    created_at timestamp default current_timestamp
);