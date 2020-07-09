CREATE TABLE Matches (
  id int NOT NULL AUTO_INCREMENT,
  date date,
  round int,
  home_team_id int,
  home_score int,
  away_team_id int,
  away_score int,
  winner int,
  is_draw boolean,
  stadium_id int,
  weather varchar(255),
  url varchar(255),
  PRIMARY KEY (id),
  FOREIGN KEY (stadium_id) REFERENCES Stadiums(id),
  FOREIGN KEY (home_team_id) REFERENCES Teams(id),
  FOREIGN KEY (away_team_id) REFERENCES Teams(id)
);
