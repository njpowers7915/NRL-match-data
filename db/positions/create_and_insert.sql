#1. Create Table
CREATE TABLE Positions (
  id int NOT NULL AUTO_INCREMENT,
  position_name varchar(30) NOT NULL,
  max_on_field int,
  is_forward boolean,
  is_back boolean,
  is_starter boolean,
  PRIMARY KEY (id)
);

#2. Insert Values
INSERT INTO Positions (position_name, max_on_field, is_forward, is_back, is_starter)
VALUES ('Fullback', 1, 0, 1, 1),
('Wing', 2, 0, 1, 1),
('Centre', 2, 0, 1, 1),
('Five-Eighth', 1, 0, 1, 1),
('Halfback', 1, 0, 1, 1),
('Prop', 2, 1, 0, 1),
('Hooker', 1, 1, 0, 1),
('2nd Row', 2, 1, 0, 1),
('Lock', 1, 1, 0, 1),
('Interchange', 4, null, null, 0);
