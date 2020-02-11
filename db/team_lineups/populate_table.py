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
mycursor.execute("USE NRL_data;")

team_match_query = pd.read_sql_query("SELECT id, home_team_id, away_team_id, winner FROM Matches;", mycursor)
team_match_df = pd.DataFrame(team_match_query, columns=['match_id', 'team_1', 'team_2', 'winner'])
lineup_query = pd.read_sql_query('''
    SELECT *
    FROM PlayerMatchStats
    WHERE match_id = {}
        AND team_id = {}
    ORDER BY position_id;''', mycursor)

stat_df = pd.read_sql_query('''
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
WHERE match_id = 1
	AND team_id = 1;''', mycursor)


mycursor.execute(get_match_url_query, )
match_list = mycursor.fetchall()


mycursor.close()
