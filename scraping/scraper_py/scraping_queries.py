import mysql.connector

def find_sql_ids(table_name, identifier, value, mycursor):
    query = """SELECT *
                FROM {table_name}
                WHERE {identifier} = '{value}'
                """
    sql_command = query.format(table_name=table_name, identifier=identifier, value=value)
    #print(sql_command)
    mycursor.execute(sql_command)
    try:
        result = mycursor.fetchone()
        id = result[0]
        return id
    except:
        id = None
        return id

#find_sql_ids("Stadiums", id, "Suncorp Stadium", mycursor)
