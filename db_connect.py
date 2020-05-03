'''
File managing all connection needs with MySQL database: Creation and updating
'''

####### IMPORTS #######
from sqlalchemy import create_engine
import pandas as pd

import service_recc as sr
import convert_sql as cs

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
Gets user's watchlist from "IMDb_Watchlist" table in database

Inputs: string username - unique to each user and finds set of watchlists
        string watchlist_name - name of watchlist set by user
Returns: Pandas.DataFrame fetched_watchlist - same format as below: with Position, Const, and Title as columns

Created by Jessica 04.29

NOTES: NEED TO CREATE UPDATE METHODS (ADD CONTENT, DELETE CONTENT, CHANGE WATCHLIST NAME)
'''
def fetch_watchlist(username, watchlist_name):
  # connect to database
  db = get_db()

  # query for watchlist information
  watchlist = db.execute('''SELECT Position, Const, Title FROM IMDb_Watchlist WHERE username="{username}" AND watchlist_name="{watchlist_name}"'''.format(username=username, watchlist_name=watchlist_name)).fetchall()

  # COME BACK LATER AND DO ERROR HANDLING IF USERNAME OR WATCHLIST_NAME INCORRECT

  # create DataFrame to return
  fetched_watchlist = pd.DataFrame(columns=['Position','Const','Title'])
  fetched_watchlist = fetched_watchlist.set_index('Position')

  # parse through query
  for title in watchlist:
    fetched_watchlist = fetched_watchlist.append({'Const':title['Const'], 'Title':title['Title']}, ignore_index=True)

  db.close()
  return fetched_watchlist

'''
Retrieves relevant watchlist info from MySQL for profile-watchlist-each.html template

Inputs: string username: unique to each user and finds set of watchlists
        string watchlist_name: name of watchlist set by user, unique within each user
Returns:pandas.DataFrame joined_frame: DataFrame of all info needed to build title cards

Created by Jessica 04.29
'''
def fetch_html_watchlist(username, watchlist_name):
  # connect to database
  db = get_db()

  # join query for watchlist information
  join_query = db.execute('''SELECT DISTINCT i.Const, i.Title, i.Year, i.Genres, i.IMDb_Rating, p.google_rent, p.google_buy, p.google_url, p.itunes_rent, p.itunes_buy, p.itunes_url, p.amazon_prime, p.netflix, p.hbo, p.hulu, p.nowhere FROM IMDb_Watchlist i LEFT JOIN Parsed_Watchlist p ON i.Const = p.imdbID WHERE p.username="{username}" AND p.watchlist_name="{watchlist_name}"'''.format(username=username, watchlist_name=watchlist_name)).fetchall()

  joined_frame = pd.DataFrame(columns=['Const','Title','Year','Genres','IMDb_Rating','google_rent','google_buy','google_url','itunes_rent','itunes_buy','itunes_url','amazon_prime','netflix','hbo','hulu','nowhere'])

  for title in join_query:
    joined_frame = joined_frame.append({'Const':title['Const'],'Title':title['Title'],'Year':title['Year'],'Genres':title['Genres'],'IMDb_Rating':title['IMDb_Rating'],'google_rent':title['google_rent'],'google_buy':title['google_buy'],'google_url':title['google_url'],'itunes_rent':title['itunes_rent'],'itunes_buy':title['itunes_buy'],'itunes_url':title['itunes_url'],'amazon_prime':title['amazon_prime'],'netflix':title['netflix'],'hbo':title['hbo'],'hulu':title['hulu'],'nowhere':title['nowhere']}, ignore_index=True)

  joined_frame = joined_frame.set_index('Const')
  db.close()
  return joined_frame

'''
Updates watchlist tables from new watchlist file uploads - creates new watchlist

Inputs: string username: unique to each user
        string watchlist_name: unique within user of new watchlist
        string file: file path to list downloaded from IMDb to upload into user's account
Returns: returns False if file not from IMDb
         returns True if able to write new watchlist into table

Created by Jessica 05.01
'''
def create_watchlist_upload(username, watchlist_name, filepath):
  # make filepath into pandas.DataFrame object
  file = pd.read_csv(filepath)
  # print(file.columns)

  # checks that content of file is really directly from IMDb
  # set of expected column names
  expected_head = {'Position','Const','Created','Modified','Description','Title','URL','Title Type','IMDb Rating','Runtime (mins)','Year','Genres','Num Votes','Release Date','Directors','Your Rating','Date Rated'}
  for col in file.columns:
    if col not in expected_head:
      return False

  # put content of table into IMDb_Watchlist
  db = get_db()

  imdb_query = '''INSERT IGNORE INTO IMDb_Watchlist (Position, username, watchlist_name, Const, Created, Modified, Description, Title, URL, Title_Type, IMDb_Rating, Runtime, Year, Genres, Num_Votes, Release_Date, Directors, Your_Rating, Date_Rated) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
  
  for index, row in file.iterrows():
    descrip = row['Description']
    if str(descrip) == "nan": descrip = ""
    directors = row['Directors']
    if str(directors) == "nan": directors = ""
    your_rating = row['Your Rating']
    if str(your_rating) == "nan": your_rating = ""
    date_rated = row['Date Rated']
    if str(date_rated) == "nan": date_rated = ""

    imdb_param = (row['Position'], username, watchlist_name, row['Const'], row['Created'], row['Modified'], descrip, row['Title'], row['URL'], row['Title Type'], row['IMDb Rating'], row['Runtime (mins)'], row['Year'], row['Genres'], row['Num Votes'], row['Release Date'], directors, your_rating, date_rated)
    db.execute(imdb_query, imdb_param)

  # put content of table into Parsed_Watchlist
  parsed_list = sr.watchlist_parse(fetch_watchlist(username, watchlist_name))
  print(parsed_list)
  cs.convert_to_sql(parsed_list, username, watchlist_name)

  db.close()
  return True



'''
Retrieves status of linked accounts from MySQL on "Linked Accounts" page

Inputs: string username: unique to each user and finds status of linked accounts
Returns: dictionary linked_status: dictionary with boolean values of if user has linked accounts. Default for new user is all false

Created by Jessica 04.30
'''
def linked_account_status(username):
  # Default user has all false values
  linked_status = {'amazon_prime': False, 'netflix': False, 'hbo': False, 'hulu': False}

  # Connect to database
  db = get_db()
  query = db.execute('''SELECT linked_amazon, linked_netflix, linked_hbo, linked_hulu FROM all_user_data WHERE username="{username}"'''.format(username=username)).fetchone()
  db.close()

  # Fill dictionary info
  if query['linked_amazon'] == 1: linked_status['amazon_prime'] = True 
  if query['linked_netflix'] == 1: linked_status['netflix'] = True
  if query['linked_hbo'] == 1: linked_status['hbo'] = True
  if query['linked_hulu'] == 1: linked_status['hulu'] = True

  return linked_status

'''
Updates linked accounts for users

Inputs: string username: unique to each user
        string service: name of service updating, by column name - 'linked_amazon', 'linked_netflix', 'linked_hbo', 'linked_hulu'
        boolean status: true if have linked account, else false
Returns:

Created by Jessica 04.30
'''
def update_account_status(username, service, status):
  # connect to database
  db = get_db()

  # Update database
  update = db.execute('''UPDATE all_user_data SET {service} = {status} WHERE username="{username}"'''.format(username=username, service=service, status=status))
  db.close()

  return





















'''
04.29 - OLD VERSION, FROM WHEN WATCHLISTS WERE SEPARATE TABLES, KEEPING FOR POTENTIAL FUTURE TESTING NEEDS

Imports IMDb watchlist table from MySQL

input: string db_watchlist: table name (test with 'IMDb_Watchlist_sample', 'IMDb_Watchlist_Jenny')
output: watchlist as a pandas dataframe with three columns: Position (index), Const, and Title

4/21 Helen
'''
def fetch_watchlist_DEP(db_watchlist):
    db = get_db()

    watchlist = pd.read_sql_table(db_watchlist,
                           db,
                           schema='streamline',
                           index_col='Position',
                           coerce_float=True,
                           columns=['Const', 'Title'],
                           parse_dates=None,
                           chunksize=None)
    db.close()
    return watchlist

#edits above by Helen 4/21--------------------------
#need watchlist, enter information from api calls
#1. get watchlist into sql
#2. call correct watchlist table and throw into api call
#3. take info from api call and throw back into sql
#4. run recommendation method 
#5. html??????????????????

'''
04.29 - OLD VERSION, FROM WHEN WATCHLISTS WERE SEPARATE TABLES, KEEPING FOR POTENTIAL FUTURE TESTING NEEDS

Retrieves relevant watchlist info from MySQL for profile-watchlist-each.html template

Input: string full_watchlist: name of table in database containing full watchlist info (ex: "IMDb_Watchlist_Jenny")
       string parsed_watchlist: name of table in database containing parsed location info for watchlist (ex. "Parsed_Watchlist_Jenny")
Returns: pandas.DataFrame join_query: DataFrame of all info needed to build title cards

Created by Jessica 04.26

NOTE: EVENTUALLY IN WHATEVER METHOD CALLS THIS, FIND WAY TO GET BOTH JUST BY USERID INFO
'''
def fetch_html_watchlist_DEP(full_watchlist, parsed_watchlist):
  # connect to database
  db = get_db()

  # construct query for content card information
  join_query = pd.read_sql_query('''SELECT f.Const, f.Title, f.Year, f.Genres, f.`IMDb Rating`, p.google_rent, p.google_buy, p.itunes_rent, p.itunes_buy, p.amazon_prime, p.netflix, p.hbo, p.hulu, p.nowhere
                    FROM {full} f LEFT JOIN {parsed} p
                    ON f.Const = p.imdbID'''.format(full=full_watchlist, parsed=parsed_watchlist),
                    db, coerce_float=False)

  join_query.rename(columns={"IMDb Rating":"IMDb_Rating"}, inplace=True)
  join_query.set_index('Const', inplace=True)
  db.close()
  return join_query