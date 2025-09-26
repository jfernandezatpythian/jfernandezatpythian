CREATE OR REPLACE PACKAGE roster_management_pkg AS
  -- Procedure to add a new team to the leagueddddddddddddfsdbssfd
  PROCEDURE add_team (
      p_team_id      IN teams.team_id%TYPE,
      p_team_name    IN teams.team_name%TYPE,
      p_stadium      IN teams.stadium%TYPE,
      p_city         IN teams.city%TYPE,
      p_founded_year IN teams.founded_year%TYPE
  );
  -- Procedure to add a new player to a specific team
  PROCEDURE add_player (
      p_player_id     IN players.player_id%TYPE,
      p_team_id       IN players.team_id%TYPE,
      p_first_name    IN players.first_name%TYPE,
      p_last_name     IN players.last_name%TYPE,
      p_position      IN players.position%TYPE,
      p_nationality   IN players.nationality%TYPE,
      p_jersey_number IN players.jersey_number%TYPE
  );
  -- Procedure to move a player from one team to another
  PROCEDURE transfer_player (
      p_player_id   IN players.player_id%TYPE,
      p_new_team_id IN players.team_id%TYPE
  );
  -- Function to get the number of players on a team
  FUNCTION get_player_count_for_team (
      p_team_id IN teams.team_id%TYPE
  ) RETURN NUMBER;
END roster_management_pkg;
/
