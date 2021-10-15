DROP TABLE IF EXISTS entries;
CREATE TABLE dataset (
 id SERIAL PRIMARY KEY,
 "array" TEXT NOT NULL,
 "result_array" TEXT NOT NULL,
 "created_on" TIMESTAMP NOT NULL
);