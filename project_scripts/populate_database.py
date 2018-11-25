import sqlite3
from create_tables import create_choc_db_tables
import csv
import json
import sys


# Part 1: Read data from CSV and JSON into a new database called choc.db
DBNAME = 'choc.db'
BARSCSV = 'flavors_of_cacao_cleaned.csv'
COUNTRIESJSON = 'countries.json'



def populate_countries(jsonFile):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    CountriesTableClms = '"Alpha2", "Alpha3", "EnglishName", "Region", "Subregion", "Population", "Area"'

    for country in jsonFile:
        sql = '''
            INSERT INTO Countries(''' + CountriesTableClms + ''') 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        '''
        cur.execute(sql, (country['alpha2Code'], country['alpha3Code'], country['name'], country['region'], 
            country['subregion'], country['population'], country['area']))

    #This makes it so there isn't an error when a county of BroadBeanOrigin is Unkown
    cur.execute(sql, ('UN', 'UNK', 'Unknown', 'Unknown', '', 0, 0))

    # commit and close changes
    conn.commit()
    conn.close()



def populate_bars(csvFile):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    # CSV file has the following column headers to grab from
    #    0              1             2         3           4              5           6        7            8 
    #  Company, SpecificBeanBarName, REF, ReviewDate, CocoaPercent, CompanyLocation, Rating, BeanType, BroadBeanOrigin
    BarsTableClms = '''
        "Company", "SpecificBeanBarName", "REF", "ReviewDate", "CocoaPercent", 
        "CompanyLocationId", "Rating", "BeanType", "BroadBeanOriginId"
    '''
    for row in csvFile:
        if row[0] != "Company":
            
            # write sql command - need to select from countries the country id
            # associated with the same english name as our .csv file
            sql = '''
                SELECT Id 
                FROM Countries 
                WHERE EnglishName="'''+row[5]+'''"
            '''
            countryId = cur.execute(sql).fetchone()[0] # execute sql cmd, and fetch the first results value

            sql = '''
                SELECT Id 
                FROM Countries 
                WHERE EnglishName="'''+row[8]+'''"
            '''
            beanId = cur.execute(sql).fetchone()[0] # execute sql cmd, and fetch the first results value

            # sql cmd to insert into bars the values from the current row of the
            # csv file, and the country id from the countries table for our foriegn keys
            sql = '''
                INSERT INTO Bars(''' + BarsTableClms + ''')  
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
            cocoa = float(row[4].split('%')[0])
            rating = float(row[6])

            # insert into values 'BarsTableClms' - if we dont specify this, we will insert into our primary key column!!
            cur.execute(sql, (row[0], row[1], row[2], row[3], cocoa,  countryId, rating, row[7], beanId))

    # commit and close changes
    conn.commit()
    conn.close()



def populate_choc_db():

    # create the countries and bars table in our database
    create_choc_db_tables()

    # open json file
    json_file = json.load(open(COUNTRIESJSON))
    populate_countries(json_file)

    # open the csv file
    csv_data = csv.reader(open(BARSCSV), delimiter=',')
    populate_bars(csv_data)
    

# RUN PART 1 
# #### COMMENT THIS OUT WHEN RUNNING TESTS!!!!!!!!!!!!!
# populate_choc_db()
# sys.exit()  #remember to remove this later!!!!!!!!!!!