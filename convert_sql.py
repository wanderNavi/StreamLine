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
    insert_query = '''INSERT IGNORE INTO {table} (position, title,google_rent, google_buy, itunes_rent, itunes_buy,
                    amazon_prime, netflix, hbo, hulu, nowhere) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''.format(table=table_name)
   
    
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
        query_parameters = (position, title, google_rent, google_buy, itunes_rent, itunes_buy, amazon_prime, netflix, hbo, hulu, nowhere)
        con.execute(insert_query, query_parameters)
        
        # end of method
    
'''
Retrieving stored table information - potential input for recommendation methods

Input: string table_name
Returns: dictionary parsed_loc

Created by Jessica - 04.21
'''        
def retrieve_from_sql(table_name):
    # Connect to database
    con = db_conn.get_db()
    
    # TO DO: proper try catch error handling
    query = '''SELECT * FROM {table}'''.format(table=table_name)
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
        if item[2] is not None:
            parsed_loc['individual']['google']['rent'][item[1]] = item[2]
        if item[3] is not None:
            parsed_loc['individual']['google']['buy'][item[1]] = item[3]
        # ITUNES
        if item[4] is not None:
            parsed_loc['individual']['itunes']['rent'][item[1]] = item[4]
        if item[5] is not None:
            parsed_loc['individual']['itunes']['buy'][item[1]] = item[5]
        
        # check and fill in subscriptions
        # AMAZON
        if item[6] == 1:
            parsed_loc['subscription']['amazon prime'].append(item[1])
        # NETFLIX
        if item[7] == 1:
            parsed_loc['subscription']['netflix'].append(item[1])
        # HBO
        if item[8] == 1:
            parsed_loc['subscription']['hbo'].append(item[1])
        # HULU
        if item[9] == 1:
            parsed_loc['subscription']['hulu'].append(item[1])
        
        # check if nowhere
        if item[10] == 1:
            parsed_loc['nowhere'].append(item[1])
           
    
    return parsed_loc











