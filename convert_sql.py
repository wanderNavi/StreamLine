#######################################################################################

'''
This file containes the method to convert the recommendation results into sql.

Broadly, file handles conversion to and from sql for further processing in project,
as in towards the recommendation algorithm or towards front-end.

Created by Kitty - Apr 20
Modified by Jessica, see notes - 04.21, 04.25
'''
#######################################################################################

import db_connect as db_conn
# Jessica - 04.25, putting all database call needs into one file

#######################################################################################
'''
This method is to convert the recommendation results into sql.

Input: dictionary parsed_loc, string table_name
Returns:

Created by Kitty - 04.20
Modified by Jessica - 04.21: 
    changing "watchlist" from pandas.Dataframe to output of sr.watchlist_parse()
    filling out documentation head
NOTED: Jessica 04.26 - we need a better way of IDing all these different watchlists - structure for table names
'''
def convert_to_sql(parsed_loc, table_name):
    # Get the parsed watchlist
#     parsed_loc = sr.watchlist_parse(watchlist)
    
    # Connect to database
    con = db_conn.get_db()
    
    # Drop the old table if exists
    drop_table_query = '''DROP table IF EXISTS {table}'''.format(table=table_name)
    con.execute(drop_table_query)
    
    # Create a new table
    create_table_query = '''CREATE TABLE IF NOT EXISTS {table} (position int, 
                         imdbID text,
                         title varchar(255),
                         google_rent real,
                         google_buy real,
                         itunes_rent real,
                         itunes_buy real,
                         amazon_prime bool,
                         netflix bool,
                         hbo bool,
                         hulu bool,
                         nowhere bool,
                         PRIMARY KEY(position, title))'''.format(table=table_name)
    con.execute(create_table_query)
    
    # Insert head into the table
    insert_query = '''INSERT IGNORE INTO {table} (position, imdbID, title, google_rent, google_buy, itunes_rent, itunes_buy,
                    amazon_prime, netflix, hbo, hulu, nowhere) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''.format(table=table_name)
   
    
    # creating set of all items - Jessica
    all_set = set()
    all_set.update(parsed_loc['individual']['google']['buy'].keys())
    all_set.update(parsed_loc['individual']['itunes']['buy'].keys())
    all_set.update(parsed_loc['subscription']['amazon prime'])
    all_set.update(parsed_loc['subscription']['netflix'])
    all_set.update(parsed_loc['subscription']['hbo'])
    all_set.update(parsed_loc['subscription']['hulu'])
    all_set.update(parsed_loc['nowhere'])
    
    # slice the dictionary
    for index, title in enumerate(all_set):
        # position
        position = index + 1
        imdbID = parsed_loc['ids'][title]
        
        # individual
        # MODIFIED by Jessica to handle cases where no ind option
        google_rent = None
        google_buy = None
        itunes_rent = None
        itunes_buy = None
        if title in parsed_loc['individual']['google']['rent']:
            google_rent = parsed_loc['individual']['google']['rent'][title]
        if title in parsed_loc['individual']['google']['buy']:
            google_buy = parsed_loc['individual']['google']['buy'][title]
        if title in parsed_loc['individual']['itunes']['rent']:
            itunes_rent = parsed_loc['individual']['itunes']['rent'][title]
        if title in parsed_loc['individual']['itunes']['buy']:
            itunes_buy = parsed_loc['individual']['itunes']['buy'][title]
        
        # subscription
        amazon_prime = True if title in parsed_loc['subscription']['amazon prime'] else False
        netflix = True if title in parsed_loc['subscription']['netflix'] else False
        hbo = True if title in parsed_loc['subscription']['hbo'] else False
        hulu = True if title in parsed_loc['subscription']['hulu'] else False
        nowhere = True if title in parsed_loc['nowhere'] else False
        
        # execute query
        query_parameters = (position, imdbID, title, google_rent, google_buy, itunes_rent, itunes_buy, amazon_prime, netflix, hbo, hulu, nowhere)
        con.execute(insert_query, query_parameters)
        
    con.close()
    # end of method
    
'''
Retrieving stored table information - potential input for recommendation methods

Input:  string username: unique username
        string table_name: already parsed watchlist - Jessica 04.30 swap out
Returns: dictionary parsed_loc

Created by Jessica - 04.21
'''        
def retrieve_from_sql(username):
    # Connect to database
    con = db_conn.get_db()
    
    # TO DO: proper try catch error handling
    query = '''SELECT DISTINCT imdbID, title, google_rent, google_buy, itunes_rent, itunes_buy, amazon_prime, netflix, hbo, hulu, nowhere FROM Parsed_Watchlist WHERE username="{username}"'''.format(username=username)
    query_ret = con.execute(query)
    
    # Constructing dictionary that will be returned
    parsed_loc = {'individual':{'google':{'rent':dict(),'buy':dict()},
                              'itunes':{'rent':dict(),'buy':dict()},
                              'amazon instant':{'rent':dict(),'buy':dict()}},
                'subscription':{'amazon prime':[],
                                'netflix':[],
                                'hbo':[],
                                'hulu':[]},
                'nowhere':[]}
    
    # headers: index, title, google_buy, google_rent, itunes_buy, 
             # itunes_rent, amazon_prime, netflix, hbo, hulu, nowhere
    # Going through each line of table 
    # NOTE: there is definitely a better way to do this
    for item in query_ret:
        # check and fill in individual 
        # GOOGLE
        if item['google_rent'] is not None:
            parsed_loc['individual']['google']['rent'][item['title']] = item['google_rent']
        if item['google_buy'] is not None:
            parsed_loc['individual']['google']['buy'][item['title']] = item['google_buy']
        # ITUNES
        if item['itunes_rent'] is not None:
            parsed_loc['individual']['itunes']['rent'][item['title']] = item['itunes_rent']
        if item['itunes_buy'] is not None:
            parsed_loc['individual']['itunes']['buy'][item['title']] = item['itunes_buy']
        
        # check and fill in subscriptions
        # AMAZON
        if item['amazon_prime'] == 1:
            parsed_loc['subscription']['amazon prime'].append({'title':item['title'],'imdbID':item['imdbID']})
        # NETFLIX
        if item['netflix'] == 1:
            parsed_loc['subscription']['netflix'].append({'title':item['title'],'imdbID':item['imdbID']})
        # HBO
        if item['hbo'] == 1:
            parsed_loc['subscription']['hbo'].append({'title':item['title'],'imdbID':item['imdbID']})
        # HULU
        if item['hulu'] == 1:
            parsed_loc['subscription']['hulu'].append({'title':item['title'],'imdbID':item['imdbID']})
        
        # check if nowhere
        if item['nowhere'] == 1:
            parsed_loc['nowhere'].append({'title':item['title'],'imdbID':item['imdbID']})
           
    con.close()
    return parsed_loc











