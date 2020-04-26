'''
File managing all connection needs with MySQL database
'''

####### IMPORTS #######
from sqlalchemy import create_engine
import pandas as pd

####### METHODS #######
'''
Creates connection to database and returns engine

Inputs: 
Returns: connected engine

Created: Jessica 04.25
'''
def get_db():
  conn_string = 'mysql+pymysql://{user}:{password}@{host}/{db}?charset={encoding}'.format(
        host = '35.245.115.59', 
        user = 'root',
        db = 'streamline',
        password = 'dwdstudent2015',
        encoding = 'utf8mb4')
  engine = create_engine(conn_string)
  return engine.connect()


'''
Imports IMDb watchlist table from MySQL

input: string db_watchlist: table name (test with 'IMDb_Watchlist_sample', 'IMDb_Watchlist_Jenny')
output: watchlist as a pandas dataframe with three columns: Position (index), Const, and Title

4/21 Helen
'''
def fetch_watchlist(db_watchlist):
    db = get_db()

    watchlist = pd.read_sql_table(db_watchlist,
                           db,
                           schema='streamline',
                           index_col='Position',
                           coerce_float=True,
                           columns=['Const', 'Title'],
                           parse_dates=None,
                           chunksize=None)
    
    return watchlist

#edits above by Helen 4/21--------------------------
#need watchlist, enter information from api calls
#1. get watchlist into sql
#2. call correct watchlist table and throw into api call
#3. take info from api call and throw back into sql
#4. run recommendation method 
#5. html??????????????????

'''
Retrieves relevant watchlist info from MySQL for profile-watchlist-each.html template

Input: string full_watchlist: name of table in database containing full watchlist info (ex: "IMDb_Watchlist_Jenny")
       string parsed_watchlist: name of table in database containing parsed location info for watchlist (ex. "Parsed_Watchlist_Jenny")
Returns: pandas.DataFrame join_query: DataFrame of all info needed to build title cards

Created by Jessica 04.26

NOTE: EVENTUALLY IN WHATEVER METHOD CALLS THIS, FIND WAY TO GET BOTH JUST BY USERID INFO
'''
def fetch_html_watchlist(full_watchlist, parsed_watchlist):
  # connect to database
  db = get_db()

  # construct query for content card information
  join_query = pd.read_sql_query('''SELECT f.Const, f.Title, f.Year, f.Genres, f.`IMDb Rating`, p.google_rent, p.google_buy, p.itunes_rent, p.itunes_buy, p.amazon_prime, p.netflix, p.hbo, p.hulu, p.nowhere
                    FROM {full} f LEFT JOIN {parsed} p
                    ON f.Const = p.imdbID'''.format(full=full_watchlist, parsed=parsed_watchlist),
                    db, coerce_float=False)

  join_query.rename(columns={"IMDb Rating":"IMDb_Rating"}, inplace=True)

  return join_query