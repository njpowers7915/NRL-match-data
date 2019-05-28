import csv

round_input = input('Round number: ')
year_input = input('Year: ')

csv_name = ('round_' + str(round_input) + '_' + str(year_input) + '.csv')

open_file = open(csv_name)
read_file = csv.reader(open_file)

for row in read_file[1:]:
    
