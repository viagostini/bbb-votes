DROP TABLE IF EXISTS participants;

CREATE TABLE participants (
    id INT GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(50) NOT NULL,
    votes INT DEFAULT 0
);

INSERT INTO participants(name)
VALUES ('The Flash');

INSERT INTO participants(name)
VALUES ('Superman');

INSERT INTO participants(name)
VALUES ('Batman');
