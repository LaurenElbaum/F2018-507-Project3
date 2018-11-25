import sqlite3
import sys

DBNAME = 'choc.db'


#
# FUNCTION: Performs given sql query and returns the tuple result
#
def perform_query(sql):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    results = cur.execute(sql)
    result_list = results.fetchall()
    conn.close()
    return result_list



#
# FUNCTION: Prepares a row of data for output to the terminal, given a one
#           dimensional tuple of length 6. The tuple is stransformed into
#           a table like structure, for easy reading by the user. 
#
def prepare_bars_output_row(data):
    return (
        ((data[0][:20] + '..').ljust(30) if len(data[0]) > 25 else data[0].ljust(30)) +
        ((data[1][:20] + '..').ljust(25) if len(data[1]) > 20 else data[1].ljust(25)) +
        ((data[2][:20] + '..').ljust(30) if len(data[2]) > 25 else data[2].ljust(30)) + 
        (str(data[3]).ljust(5)) +
        ((str(data[4]) + '%').ljust(8)) +
        ((data[5][:20] + '..').ljust(25) if len(data[5]) > 25 else data[5].ljust(25))
    )



#
# FUNCTION: Processes and interprets bars command parameters.
#           Handles invalid parameters for Bars command
#
def process_bars_command(params):

    #error check, bars command takes at most 3 paramaters
    if len(params) > 3:
        return ('error', 'Command "Bars" takes at most 3 parameters.')

    # SQL query stub. the following is present in every query for bars
    sql = '''
        SELECT SpecificBeanBarName,
               Company,
               C1.EnglishName AS country,
               Rating, CocoaPercent,
               C2.EnglishName AS origin
        FROM Bars 
        JOIN Countries AS C1 ON Bars.CompanyLocationId=C1.Id
        JOIN Countries AS C2 ON Bars.BroadBeanOriginId=C2.Id
    '''

    # default values as specified by spec!!
    where   = ''                   # No default - dont require filter
    orderBy = ' ORDER BY RATING'   # Default value to order results by
    limit   = ' DESC LIMIT 10'     # default value for how many results to show

    # variables to check for duplicate paramter types
    whereSet   = 0
    limitSet   = 0
    orderBySet = 0

    # loop through and interpret each parameter
    for option in params:

        # conditional checks for filters/limits.
        if len(option.split('=')) == 2:
            if option.split('=')[0] == 'sellcountry':
                where += ' WHERE C1.Alpha2="' + option.split('=')[1] + '"'
                whereSet += 1

            elif option.split('=')[0] == 'sellregion':
                where += ' WHERE C1.Region="' + option.split('=')[1] + '"'
                whereSet += 1

            elif option.split('=')[0] == 'sourcecountry':
                where += ' WHERE C2.Alpha2="' + option.split('=')[1] + '"'
                whereSet += 1

            elif option.split('=')[0] == 'sourceregion':
                where += ' WHERE C2.Region="' + option.split('=')[1] + '"'
                whereSet += 1
    
            elif option.split('=')[0] == 'top':
                limit = ' DESC LIMIT ' + option.split('=')[1]
                limitSet += 1

            elif option.split('=')[0] == 'bottom':
                limit = ' ASC LIMIT ' + option.split('=')[1]
                limitSet += 1

            # filter or limit parameter not recognized - return erropr
            else:
                return('error', 'Parameter with value"' + option + '" not recognized. Please try again.')
    

        # check for / interpret order by parameters
        elif option == 'ratings':
            orderBy = ' ORDER BY RATING'
            orderBySet += 1

        elif option == 'cocoa':
            orderBy = ' ORDER BY CocoaPercent'
            orderBySet += 1

        # paramater not recognized as valid bars param - return error
        else:
            return('error', 'Parameter "' + option + '" not recognized. Please try again.')


        # Check for duplicate param types. If duplictes, return error
        if whereSet > 1 or limitSet > 1 or orderBySet > 1:
            return('error', 'Multiple filter options not allowed.')


    sql += where + orderBy + limit 
    return perform_query(sql)
