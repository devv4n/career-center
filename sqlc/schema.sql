create table if not exists vacancies (
    id integer primary key,
    name varchar(255) not null,
    description varchar(255) unique not null,
    email varchar(32),
    created_at timestamp not null,
    updated_at timestamp not null,
    show boolean default false
);

create table if not exists events (
    id integer primary key,
    name varchar(255) not null,
    description varchar(255) unique not null,
    image varchar(32),
    date timestamp not null,
    created_at timestamp not null,
    updated_at timestamp not null
);