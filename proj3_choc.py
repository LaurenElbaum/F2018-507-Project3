import sqlite3
import sys


sys.path.append('./project_scripts')

# PART 1 SCRIPTS
from populate_database import *
from create_tables import *

#PART 2 SCRIPTS
from command_bars import *
from command_companies import *
from command_countries import *
from command_regions import *




# proj3_choc.py
# You can change anything in this file you want as long as you pass the tests
# and meet the project requirements! You will need to implement several new
# functions.

# Part 1: Read data from CSV and JSON into a new database called choc.db
populate_choc_db() # call to populate db



# Part 2: Implement logic to process user commands

#
# FUNCTION: Given a command, function prepares additional paramaters and
#           calls corresponding command function interpreter. Returns
#           the query results returned by corresponding command function interpreter.
#
#           command: string -> with value of bars, companies, regions, or countries.
#                    Otherwise, an error result is returned for unrecognized command.
#
def process_command(command):
    if  command == '':
        return ('empty', '')

    params = command.split()  # get array of user input

    if params[0].lower() == 'exit':
        return ('exit')

    elif params[0].lower() == 'bars':
        return process_bars_command(params[1:])

    elif params[0].lower() == 'companies':
        return process_companies_command(params[1:])

    elif params[0].lower() == 'countries':
        return process_countries_command(params[1:])

    elif params[0].lower() == 'regions':
        return process_regions_command(params[1:])

    else:
        return ('error', 'Command "' + params[0] + '" unknown. Please try again.')





#
# FUNCTION: Given a 2 dimensional tuple of query results, function prepares
#           said results for user friendly output to the terminal. 
#
#           cmd: the command used by user, either bars, countries, companies, or regions
#           percent: boolean true if results contain percent value column, false otherwise
#           percent: boolean true if results contain a count value column, false otherwise
#
def output_results(results, cmd, percent, count):

    # Errors come in as tuples, where the 0th value is 'error', [1] value is msg
    if results[0] == 'error':
        print('ERROR: =>', results[1], '\n')
        return

    output = '' # String that holds transformed row data for pretty printing 

    if cmd == 'bars':
        for row in results:
            output += prepare_bars_output_row(row)
            output += '\n'

    if cmd == 'companies':
        for row in results:
            output += prepare_companies_output_row(row, percent, count)
            output += '\n'

    if cmd == 'countries':
        for row in results:
            output += prepare_countries_output_row(row, percent, count)
            output += '\n'
    
    if cmd == 'regions':
        for row in results:
            output += prepare_regions_output_row(row, percent, count)
            output += '\n'
                
    print(output)
    print('') # add an extra line for space between commands



#
# FUNCTION: Given -> prints instructions to user in terminal
#
def load_help_text():
    with open('help.txt') as f:
        return f.read()



# Part 3: Implement interactive prompt.
def interactive_prompt():
    help_text = load_help_text()
    response = ''
    while response != 'exit':
        response = input('Enter a command: ')

        if response == 'help':
            print(help_text)
            continue
        
        else:
            # process the users command string
            results = process_command(response)

            # check if percent in param - effects output in output_results function
            percent = False
            count = False
            for param in response.split():
                if param == 'cocoa':
                    percent = True

                if param == 'bars_sold':
                    count = True
            
            if not results:
                print("Empty query, try again.")
                continue

            if results[0] != 'empty':
                output_results(results, response.split()[0].lower(), percent, count)


# Make sure nothing runs or prints out when this file is run as a module
if __name__=="__main__":
    interactive_prompt()