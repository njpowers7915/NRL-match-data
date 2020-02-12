#SQL Imports
import mysql.connector
#Pandas imports
import pandas as pd

mydb = mysql.connector.connect(
  host="localhost",
  user=os.getenv("DB_USER"),
  passwd=os.getenv("DB_PASSWORD"),
  database="NRL_data"
)
mycursor = mydb.cursor()

#Queries
team_match_query = "SELECT id, home_team_id, away_team_id, winner FROM Matches;"

team_stat_query = '''
SELECT SUM(points) as points,
	SUM(tries) as tries,
    SUM(conversions) as conversions,
    SUM(penalty_goals) as penalty_goals,
    (SUM(conversions) / SUM(conversion_attempts)) as conversion_percentage,
    SUM(field_goals) as field_goals,
    SUM(total_runs) as runs,
    SUM(total_run_metres) as run_metres,
    (SUM(total_run_metres) / SUM(total_runs)) as metres_per_run,
    SUM(kick_return_metres) as kick_return_metres,
    SUM(post_contact_metres) as post_contact_metres,
    SUM(line_breaks) as line_breaks,
    SUM(line_engaged_runs) as line_engaged_runs,
    SUM(tackle_breaks) as tackle_breaks,
    SUM(hit_ups) as hit_ups,
    SUM(dummy_half_runs) as dummy_half_runs,
    SUM(offloads) as offloads,
    SUM(passes) as passes,
    SUM(tackles_made) as tackles_made,
    SUM(tackles_missed) as tackles_missed,
    SUM(ineffective_tackles) as ineffective_tackles,
    (SUM(tackles_made) / (SUM(tackles_made) + SUM(tackles_missed) + SUM(ineffective_tackles))) as tackle_percentage,
    SUM(kicks) as kicks,
    SUM(kicking_metres) as kicking_metres,
    (SUM(kicking_metres) / SUM(kicks)) as metres_per_kick,
    SUM(errors) as errors,
    SUM(handling_errors) as handling_errors,
    SUM(penalties) as penalties,
    SUM(sin_bins) as sin_bins,
    SUM(send_offs) as send_offs
FROM PlayerMatchStats
WHERE match_id = %s
	AND team_id = %s;
'''

lineup_query = '''
    SELECT player_id
    FROM PlayerMatchStats
    WHERE match_id = %s
        AND team_id = %s
    ORDER BY position_id, minutes_played DESC;'''

#Function to format results and insert into database
def format_and_insert_team_stats(match_id, team_id, opponent_id, is_winner, stat_results, lineup_results):
    points = stat_results[0]
    tries = stat_results[1]
    conversions = stat_results[2]
    penalty_goals = stat_results[3]
    conversion_percentage = stat_results[4]
    field_goals = stat_results[5]
    runs = stat_results[6]
    run_metres = stat_results[7]
    metres_per_run = stat_results[8]
    kick_return_metres = stat_results[9]
    post_contact_metres = stat_results[10]
    line_breaks = stat_results[11]
    line_engaged_runs = stat_results[12]
    tackle_breaks = stat_results[13]
    hit_ups = stat_results[14]
    dummy_half_runs = stat_results[15]
    offloads = stat_results[16]
    passes = stat_results[17]
    tackles = stat_results[18]
    missed_tackles = stat_results[19]
    ineffective_tackles = stat_results[20]
    tackle_percentage = stat_results[21]
    kicks = stat_results[22]
    kicking_metres = stat_results[23]
    metres_per_kick = stat_results[24]
    errors = stat_results[25]
    handling_errors = stat_results[26]
    penalties = stat_results[27]
    sin_bins = stat_results[28]
    send_offs = stat_results[29]

    fullback = lineup_results[0][0]
    wing_1 = lineup_results[1][0]
    wing_2 = lineup_results[2][0]
    centre_1 = lineup_results[3][0]
    centre_2 = lineup_results[4][0]
    five_eighth = lineup_results[5][0]
    halfback = lineup_results[6][0]
    prop_1 = lineup_results[7][0]
    prop_2 = lineup_results[8][0]
    hooker = lineup_results[9][0]
    sr_1 = lineup_results[10][0]
    sr_2 = lineup_results[11][0]
    lock_1 = lineup_results[12][0]
    int_1 = lineup_results[13][0]
    int_2 = lineup_results[14][0]
    try:
        int_3 = lineup_results[15][0]
    except:
        int_3 = None
    try:
        int_4 = lineup_results[16][0]
    except:
        int_4 = None
    values = (match_id, team_id, opponent_id, is_winner, points, tries, conversions, penalty_goals, conversion_percentage, field_goals, runs, run_metres, metres_per_run, kick_return_metres, post_contact_metres, line_breaks, line_engaged_runs, tackle_breaks, hit_ups, dummy_half_runs, offloads, passes, tackles, missed_tackles, ineffective_tackles, tackle_percentage, kicks, kicking_metres, metres_per_kick, errors, handling_errors, penalties, sin_bins, send_offs, fullback, wing_1, wing_2, centre_1, centre_2, five_eighth, halfback, prop_1, prop_2, hooker, sr_1, sr_2, lock_1, int_1, int_2, int_3, int_4)

    insert_query = '''INSERT INTO TeamMatchStats (match_id, team_id, opponent_id, is_winner, points, tries, conversions, penalty_goals, conversion_percentage, field_goals, runs, run_metres, metres_per_run, kick_return_metres, post_contact_metres, line_breaks, line_engaged_runs, tackle_breaks, hit_ups, dummy_half_runs, offloads, passes, tackles, missed_tackles, ineffective_tackles, tackle_percentage, kicks, kicking_metres, metres_per_kick, errors, handling_errors, penalties, sin_bins, send_offs, fullback, wing_1, wing_2, centre_1, centre_2, five_eighth, halfback, prop_1, prop_2, hooker, sr_1, sr_2, lock_1, int_1, int_2, int_3, int_4)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
'''
    mycursor.execute(insert_query, (values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7], values[8], values[9], values[10], values[11], values[12], values[13], values[14], values[15], values[16], values[17], values[18], values[19], values[20], values[21], values[22], values[23], values[24], values[25], values[26], values[27], values[28], values[29], values[30], values[31], values[32], values[33], values[34], values[35], values[36], values[37], values[38], values[39], values[40], values[41], values[42], values[43], values[44], values[45], values[46], values[47], values[48], values[49], values[50],))
    mydb.commit()

#Execution
mycursor.execute("USE NRL_data;")

#Get list of each team who played in each match
mycursor.execute(team_match_query)
team_match_results = mycursor.fetchall()

#Loop through each maatch and insert stats for each team
for result in team_match_results[2:]:
    match_id = result[0]
    for team in [result[1], result[2]]:
        team_id = team
        is_winner = team_id == result[3]
        if team == result[1]:
            opponent_id = result[2]
        else:
            opponent_id = result[1]
        #Get match stats
        mycursor.execute(team_stat_query, (match_id, team_id))
        stat_results = mycursor.fetchone()
        #Get lineup
        mycursor.execute(lineup_query, (match_id, team_id))
        lineup_results = mycursor.fetchall()
        #Format all relevant data and insert
        format_and_insert_team_stats(match_id, team_id, opponent_id, is_winner, stat_results, lineup_results)

mycursor.close()
