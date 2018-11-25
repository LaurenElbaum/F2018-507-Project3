import sqlite3 as sqlite

DBNAME = 'choc.db'

def create_choc_db_tables():

    # Connect to database
    conn = sqlite.connect(DBNAME)
    cur = conn.cursor()

    statement = "DROP TABLE IF EXISTS 'Bars';"
    cur.execute(statement)

    statement = "DROP TABLE IF EXISTS 'Countries';"
    cur.execute(statement)

    conn.commit()

    statement = '''
        CREATE TABLE 'Countries' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'Alpha2' TEXT NOT NULL,
            'Alpha3' TEXT NOT NULL,
            'EnglishName' TEXT NOT NULL,
            'Region' TEXT NOT NULL,
            'Subregion' TEXT,
            'Population' TEXT,
            'Area' TEXT 
        );
    '''

    cur.execute(statement)

    conn.commit()

    statement = '''
        CREATE TABLE 'Bars' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'Company' TEXT NOT NULL,
            'SpecificBeanBarName' TEXT NOT NULL,
            'REF' TEXT NOT NULL,
            'ReviewDate' TEXT NOT NULL,
            'CocoaPercent' REAL,
            'CompanyLocationId' INTEGER REFERENCES Countries(Id),
            'Rating' REAL,
            'BeanType' TEXT,
            'BroadBeanOriginId' INTEGER REFERENCES Countries(Id)
        );
    '''

    cur.execute(statement)
    conn.commit()
    conn.close()
