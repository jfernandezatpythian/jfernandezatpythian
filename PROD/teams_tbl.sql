CREATE TABLE teams (
    team_id      NUMBER(4) PRIMARY KEY,
    team_name    VARCHAR2(50) NOT NULL UNIQUE,
    stadium      VARCHAR2(50),
    city         VARCHAR2(50),
    founded_year NUMBER(4)
);
