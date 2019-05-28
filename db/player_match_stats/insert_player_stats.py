import csv
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="NYg1@nts",
  database="NRL_data"
)
mycursor = mydb.cursor(buffered=True)


round_input = input('Round number: ')
year_input = input('Year: ')

csv_name = ('../../scraping/scraper_py/round_' + str(round_input) + '_' + str(year_input) + '.csv')

open_file = open(csv_name)
read_file = list(csv.reader(open_file))

for i in read_file[1:]:
    for each in i:
        if each == '':
            each = 0
    result_tuple = (i[3],
    i[1],
    i[2],
    i[58],
    i[6],
    i[7],
    i[8],
    i[9],
    i[10],
    i[11],
    i[12],
    i[13],
    i[15],
    i[16],
    i[17],
    i[18],
    i[19],
    i[20],
    i[21],
    i[22],
    i[23],
    i[24],
      i[25],
      i[26],
      i[27],
      i[28],
      i[29],
      i[30],
      i[31],
      i[32],
      i[33],
      i[34],
      i[35],
      i[36],
      i[37],
      i[38],
      i[39],
      i[40],
      i[41],
      i[42],
      i[43],
      i[44],
      i[45],
      i[46],
      i[47],
      i[48],
      i[49],
      i[50],
    i[51],
    i[52],
    i[53],
    i[54],
    i[55],
    i[56],
    i[57])
    query = '''INSERT INTO PlayerMatchStats (match_id, player_id, team_id, position_id, minutes_played,
    points, tries, conversions, conversion_attempts, penalty_goals,
    conversion_percentage, field_goals, total_runs, total_run_metres, kick_return_metres,
    post_contact_metres, line_breaks, line_break_assists, try_assists, line_engaged_runs,
    tackle_breaks, hit_ups, play_the_ball, average_play_ball_seconds, dummy_half_runs,
    dummy_half_run_metres, steals, offloads, dummy_passes, passes,
    receipts, pass_to_run_ratio, tackle_percentage, tackles_made, tackles_missed, ineffective_tackles,
    intercepts, kicks_defused, kicks, kicking_metres, forced_drop_outs,
    bomb_kicks, grubbers, fourty_twenty, cross_field_kicks, kicked_dead,
    errors, handling_errors, one_on_ones_lost, penalties, on_report,
    sin_bins, send_offs, stint_one, stint_two)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    '''
    mycursor.execute(query, result_tuple)
    mydb.commit()
    print('success!')


'''
    i

    for row in reader[0]:
        print (str(i) + '--' + str(row[0])
        i += 1

(match_id = i[3],
player_id = i[1],
team_id = i[2],
position_id = i[58],
minutes_played = i[6],
points = i[7],
tries = i[8],
conversions = i[9],
conversion_attempts = i[10],
penalty_goals = i[11],
conversion_percentage = i[12],
field_goals = i[13],
total_runs = i[15],
total_run_metres = i[16],
kick_return_metres = i[17],
post_contact_metres = i[18],
line_breaks = i[19],
line_break_assists = i[20],
try_assists = i[21],
line_engaged_runs = i[22],
tackle_breaks = i[23],
hit_ups = i[24],
play_the_ball = i[25],
average_play_ball_seconds = i[26],
dummy_half_runs = i[27],
dummy_half_run_metres = i[28],
steals = i[29],
offloads = i[30],
dummy_passes = i[31],
passes = i[32],
receipts = i[33],
pass_to_run_ratio = i[34],
tackle_percentage = i[35],
tackles_made = i[36],
tackles_missed = i[37],
ineffective_tackles = i[38],
intercepts = i[39],
kicks_defused = i[40],
kicks = i[41],
kicking_metres = i[42],
forced_drop_outs = i[43],
bomb_kicks = i[44],
grubbers = i[45],
fourty_twenty = i[46],
cross_field_kicks = i[47],
kicked_dead = i[48],
errors = i[49],
handling_errors = i[50],
one_on_ones_lost = i[51],
penalties = i[52],
on_report = i[53],
sin_bins = i[54],
send_offs = i[55],
stint_one = i[56],
stint_two = i[57])
'''
