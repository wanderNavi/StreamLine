'''
File managing all connection needs with MySQL database
'''

####### IMPORTS #######
from sqlalchemy import create_engine

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
4/21 Helen
Imports IMDb watchlist table from MySQL
input: table name as db_watchlist (test with 'IMDb_Watchlist_sample', 'IMDb_Watchlist_Jenny')
output: watchlist as a pandas dataframe with three columns: Position (index), Const, and Titlev
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



