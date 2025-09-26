CREATE TABLE players (
    player_id     NUMBER(6) PRIMARY KEY,
    team_id       NUMBER(4) NOT NULL,
    first_name    VARCHAR2(50) NOT NULL,
    last_name     VARCHAR2(50) NOT NULL,
    position      VARCHAR2(20) CHECK(position IN ('Goalkeeper', 'Defender', 'Midfielder', 'Forward')),
    nationality   VARCHAR2(50),
    jersey_number NUMBER(2),
    CONSTRAINT fk_players_team FOREIGN KEY (team_id) REFERENCES teams(team_id)
);
