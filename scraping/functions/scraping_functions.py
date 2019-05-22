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
