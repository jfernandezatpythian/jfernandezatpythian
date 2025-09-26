CREATE TABLE matches (
    match_id         NUMBER(8) PRIMARY KEY,
    home_team_id     NUMBER(4) NOT NULL,
    away_team_id     NUMBER(4) NOT NULL,
    match_date       DATE,
    home_team_score  NUMBER(2) DEFAULT 0,
    away_team_score  NUMBER(2) DEFAULT 0,
    CONSTRAINT fk_matches_home_team FOREIGN KEY (home_team_id) REFERENCES teams(team_id),
    CONSTRAINT fk_matches_away_team FOREIGN KEY (away_team_id) REFERENCES teams(team_id)
);
