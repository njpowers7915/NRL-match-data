from wtforms import Form, StringField, SelectField

class PlayerSearchForm(Form):
    choices = [('player1', 'team_id1'),
               ('player2', 'team_id2')]
    select = SelectField('Search for players:', choices=choices)
    search = StringField('')
