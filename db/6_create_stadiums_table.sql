CREATE TABLE Stadiums (
  id int NOT NULL AUTO_INCREMENT,
  name varchar(255) NOT NULL UNIQUE,
  city varchar(50),
  state varchar(50),
  country varchar(50),
  PRIMARY KEY (id)
);
