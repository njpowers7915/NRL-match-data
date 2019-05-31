# Example = Leeson Ah Mau
# Currently in DB with id = 229, 485, and 1626

--Check PlayerMatchStats to see that he should be id 1626
UPDATE Players
SET is_active = 1, height_cm = 185, weight_kg = 111, city = 'Auckland',
  country = NZ, previous_team1 = 14
WHERE id = 1626;

--Update PlayerMatchStats so all entries equal the same id
UPDATE PlayerMatchStats
SET player_id = 1626
WHERE player_id IN (229, 485);

--Remove duplicate entries
DELETE FROM Players WHERE id IN (229, 485);
