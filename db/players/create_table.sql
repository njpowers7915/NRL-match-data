CREATE TABLE Players (
  id int NOT NULL AUTO_INCREMENT,
  first_name varchar(255),
  last_name varchar(255),
  is_active boolean,
  current_team int,
  height_cm int,
  weight_kg int,
  date_of_birth date,
  city varchar(255),
  state varchar(255),
  country varchar(50),
  url varchar(255),
  PRIMARY KEY (id),
  FOREIGN KEY (current_team) REFERENCES Teams(id),
  FOREIGN KEY (country_id) REFERENCES Countries(id)
);
