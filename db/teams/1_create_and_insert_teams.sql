#1. Create Table
CREATE TABLE Teams (
  id int NOT NULL AUTO_INCREMENT,
  official_name varchar(30) NOT NULL UNIQUE,
  nickname varchar(30) NOT NULL UNIQUE,
  abbreviation varchar(3),
  logo_image varchar(255),
  url varchar(255),
  PRIMARY KEY (id)
);

#2. Insert Values
INSERT INTO Teams (official_name, nickname, abbreviation)
VALUES ('Brisbane', 'Broncos', 'BRI'),
('Canberra', 'Raiders', 'CBR'),
('Canterbury-Bankstown', 'Bulldogs', 'CBY'),
('Cronulla-Sutherland', 'Sharks', 'CRO'),
('Gold Coast', 'Titans', 'GLD'),
('Manly Warringah', 'Sea Eagles', 'MAN'),
('Melbourne', 'Storm', 'MEL'),
('Newcastle', 'Knights', 'NEW'),
('New Zealand', 'Warriors', 'WAR'),
('North Queensland', 'Cowboys', 'NQL'),
('Parramatta', 'Eels', 'PAR'),
('Penrith', 'Panthers', 'PEN'),
('South Sydney', 'Rabbitohs', 'SOU'),
('St. George Illawarra', 'Dragons', 'STI'),
('Sydney', 'Roosters', 'SYD'),
('Wests', 'Tigers', 'WST');
