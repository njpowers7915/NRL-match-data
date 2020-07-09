-- Example player: Leeson Ah Mau
-- There were 3 records in the DB for this player each corresponding to a different
-- team he was playing for over the course of 2018 and 2019
-- Currently in DB with id = 229, 485, and 1626

-- 1. Check PlayerMatchStats to see that his most recent entry corresponds with id 1626
UPDATE Players
SET is_active = 1, height_cm = 185, weight_kg = 111, city = 'Auckland',
  country = NZ, previous_team1 = 14
WHERE id = 1626;

-- 2. Update PlayerMatchStats so all of his entries correspond to 1626
UPDATE PlayerMatchStats
SET player_id = 1626
WHERE player_id IN (229, 485);

-- 3. Remove duplicate entries
DELETE FROM Players WHERE id IN (229, 485);
