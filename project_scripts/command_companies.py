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
#           dimensional tuple of length 3. The tuple is stransformed into
#           a table like structure, for easy reading by the user. 
#
def prepare_companies_output_row(data, percent, count):
    output = (
        ((data[0][:20] + '..').ljust(30) if len(data[0]) > 25 else data[0].ljust(30)) 
        + ((data[1][:20] + '..').ljust(30) if len(data[1]) > 25 else data[1].ljust(30))
    )
    if percent:
        output += (str(round(data[2], 1)) + '%').ljust(8)

    elif count:
        output += str(data[2]).ljust(5)

    else:
        output += (str(round(data[2],1)) if len(str(data[2]).split('.')[1]) > 1 else str(data[2]))
    
    return(output)



#
# FUNCTION: Processes and interprets bars command parameters.
#           Handles invalid parameters for Bars command
#
def process_companies_command(params):

    #error check, bars command takes at most 3 paramaters
    if len(params) > 3:
        return ('error', 'Command "Companies" takes at most 3 parameters.')

    # SQL query stubs. the following is present in every query for bars
    sql1 = 'select Company, C1.EnglishName AS Country,'
    sql2 = ' FROM Bars Join Countries AS C1 ON Bars.CompanyLocationId=C1.Id'
    sql3 = ' GROUP BY Company HAVING COUNT(*) > 4'

    # default values as specified by spec!!
    where   = ''                   # No default - dont require filter
    column  = ' AVG(Rating)'       # Default 3rd row to average rating
    orderBy = ' ORDER BY AVG(Rating)'   # Default value to order results by
    limit   = ' DESC LIMIT 10'     # default value for how many results to show

    # variables to check for duplicate paramter types
    whereSet   = 0
    limitSet   = 0
    orderBySet = 0

    # loop through and interpret each parameter
    for option in params:

        # conditional checks for filters/limits.
        if len(option.split('=')) == 2:
            if option.split('=')[0] == 'country':
                where += ' WHERE C1.Alpha2="' + option.split('=')[1] + '"'
                whereSet += 1

            elif option.split('=')[0] == 'region':
                where += ' WHERE C1.Region="' + option.split('=')[1] + '"'
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
            column = ' AVG(Rating)'
            orderBy = ' ORDER BY AVG(Rating)'
            orderBySet += 1

        elif option == 'cocoa':
            column = ' AVG(CocoaPercent)'
            orderBy = ' ORDER BY AVG(CocoaPercent)'
            orderBySet += 1

        elif option == 'bars_sold':
            column = ' COUNT(*)'
            orderBy = ' ORDER BY COUNT(*)'
            orderBySet += 1

        # paramater not recognized as valid bars param - return error
        else:
            return('error', 'Parameter "' + option + '" not recognized. Please try again.')


        # Check for duplicate param types. If duplictes, return error
        if whereSet > 1 or limitSet > 1 or orderBySet > 1:
            return('error', 'Multiple filter options not allowed.')


    # concactenate sql stubs and param interpretations for query
    sql = sql1 + column + sql2 + where + sql3 + orderBy + limit 
    return perform_query(sql)
