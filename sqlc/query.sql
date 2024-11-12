
-- name: InsertVacancies :one
insert into vacancies (id, name, description, email, created_at, updated_at) values ($1, $2, $3, $4, current_timestamp, current_timestamp) returning id;

-- name: ListEvents :many
SELECT * FROM events ORDER BY id DESC LIMIT $1 OFFSET $2;

-- name: ListVacancies :many
select * from vacancies ORDER BY id DESC LIMIT $1 OFFSET $2;

-- name: InsertEvents :one
insert into events (id, name, description, date, created_at, updated_at) values ($1, $2, $3, $4, current_timestamp, current_timestamp) returning id;

