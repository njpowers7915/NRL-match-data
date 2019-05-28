#Insert into PlayerMatchStats
def insert_into_playerMatchStats(p):
    result_tuple = (p['match_id'],
    p['team_id'],
    p['position_id'],
    p['minutes_played'],
    p['points'],
    p['tries'],
    p['conversions'],
    p['conversion_attempts'],
    p['penalty_goals'],
    p['conversion_percentage'],
    p['field_goals'],
    p['total_runs'],
    p['total_run_metres'],
    p['kick_return_metres'],
    p['post_contact_metres'],
    p['line_breaks'],
    p['line_break_assists'],
    p['try_assists'],
    p['line_engaged_runs'],
    p['tackle_breaks'],
    p['hit_ups'],
    p['play_the_ball'],
    p['average_play_the_ball_seconds'],
    p['dummy_half_runs'],
    p['dummy_half_run_metres'],
    p['steals'],
    p['offloads'],
    p['dummy_passes'],
    p['passes'],
    p['receipts'],
    p['pass_to_run_ratio'],
    p['tackle_percentage'],
    p['tackles_made'],
    p['tackles_missed'],
    p['intercepts'],
    p['kicks_defused'],
    p['kicks'],
    p['kicking_metres'],
    p['forced_drop_outs'],
    p['bomb_kicks'],
    p['grubbers'],
    p['fourty_twenty'],
    p['cross_field_kicks'],
    p['kicked_dead'],
    p['errors'],
    p['handling_errors'],
    p['one_on_ones_lost'],
    p['penalties'],
    p['on_report'],
    p['sin_bins'],
    p['send_offs'],
    p['stint_one'],
    p['stint_two'])
    query = '''INSERT INTO PlayerMatchStats (match_id, team_id, position_id, minutes_played, points, tries,
    conversions, penalty_goals, conversion_percentage, field_goals, total_runs, total_run_metres,
    kick_return_metres, post_contact_metres, line_breaks, line_break_assists, try_assists,
    line_engaged_runs, tackle_breaks, hit_ups, play_the_ball, average_play_the_ball_seconds,
    dummy_half_runs, dummy_half_run_metres, steals, offloads, dummy_passes, passes, receipts,
    pass_to_run_ratio, tackle_percentage, tackles_made, tackles_missed, incercepts, kicks_defused,
    kicks, kicking_metres, forced_drop_outs, bomb_kicks, grubbers, fourty_twenty, cross_field_kicks,
    kicked_dead, errors, handling_errors, one_on_ones_lost, penalties, on_report, sin_bins, send_offs)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    '''

    mycursor.execute(query, result_tuple)
    mycursor.commit()
    print('success!')



#Find Team or Position ID
def find_id(table, identifier, value):
    if table == 'Teams':
        identifier = 'nickname'
    elif table == 'Positions':
        identifier = 'position_name'
    find_team_query = 'SELECT id FROM %s WHERE %s = %s;'
    mycursor.execute(find_team_query, (table, identifier, value))
    return mycursor.fetchone()[0]

#Find or Create Player by Name / Team combination
def find_or_create_player(first_name, last_name, team_id):
    find_player_query = 'SELECT id FROM Players WHERE first_name = %s AND last_name = %s AND current_team = %s LIMIT 1;'
    mycursor.execute(find_player_query, (first_name, last_name, team_id))
    result = mycursor.fetchone()
    if result is None:
        insert_player_query = 'INSERT INTO Players (first_name, last_name, current_team) VALUES (%s, %s, %s);'
        data = (first_name, last_name, team_id)
        mycursor.execute(insert_player_query, data)
        mydb.commit()
        result = find_or_create_player(first_name, last_name, team_id)
        return result
    else:
        result = result[0]
        return int(result)
