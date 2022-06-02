
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

DROP TABLE IF EXISTS student;
CREATE TABLE student (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    surname VARCHAR (32),
    name VARCHAR (32),
    patronymic VARCHAR (32),
    age INTEGER
    );

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
