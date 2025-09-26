CREATE TABLE player_match_stats (
    stat_id          NUMBER(10) PRIMARY KEY,
    match_id         NUMBER(8) NOT NULL,
    player_id        NUMBER(6) NOT NULL,
    goals_scored     NUMBER(2) DEFAULT 0,
    assists          NUMBER(2) DEFAULT 0,
    yellow_cards     NUMBER(1) DEFAULT 0,
    red_cards        NUMBER(1) DEFAULT 0,
    minutes_played   NUMBER(3) DEFAULT 0,
    CONSTRAINT fk_stats_match FOREIGN KEY (match_id) REFERENCES matches(match_id),
    CONSTRAINT fk_stats_player FOREIGN KEY (player_id) REFERENCES players(player_id),
    CONSTRAINT uq_player_match UNIQUE (match_id, player_id)
);
