CREATE OR REPLACE PACKAGE BODY roster_management_pkg AS

  PROCEDURE add_team (
      p_team_id      IN teams.team_id%TYPE,
      p_team_name    IN teams.team_name%TYPE,
      p_stadium      IN teams.stadium%TYPE,
      p_city         IN teams.city%TYPE,
      p_founded_year IN teams.founded_year%TYPE
  ) IS
  BEGIN
    INSERT INTO teams (team_id, team_name, stadium, city, founded_year)
    VALUES (p_team_id, p_team_name, p_stadium, p_city, p_founded_year);
    COMMIT;
  END add_team;

  PROCEDURE add_player (
      p_player_id     IN players.player_id%TYPE,
      p_team_id       IN players.team_id%TYPE,
      p_first_name    IN players.first_name%TYPE,
      p_last_name     IN players.last_name%TYPE,
      p_position      IN players.position%TYPE,
      p_nationality   IN players.nationality%TYPE,
      p_jersey_number IN players.jersey_number%TYPE
  ) IS
  BEGIN
    INSERT INTO players (player_id, team_id, first_name, last_name, position, nationality, jersey_number)
    VALUES (p_player_id, p_team_id, p_first_name, p_last_name, p_position, p_nationality, p_jersey_number);
    COMMIT;
  END add_player;

  PROCEDURE transfer_player (
      p_player_id   IN players.player_id%TYPE,
      p_new_team_id IN players.team_id%TYPE
  ) IS
  BEGIN
    UPDATE players
    SET team_id = p_new_team_id
    WHERE player_id = p_player_id;
    COMMIT;
  END transfer_player;

  FUNCTION get_player_count_for_team (
      p_team_id IN teams.team_id%TYPE
  ) RETURN NUMBER IS
    v_player_count NUMBER;
  BEGIN
    SELECT COUNT(*)
    INTO v_player_count
    FROM players
    WHERE team_id = p_team_id;
    
    RETURN v_player_count;
  END get_player_count_for_team;

END roster_management_pkg;
/
