############################### IMPORTS ###############################
from bs4 import BeautifulSoup
import re
import requests
import pandas as pd
# above from Jessica 04.20

############################### GLOBAL VARIABLES ###############################
UTELLY_URL = "https://utelly-tv-shows-and-movies-availability-v1.p.rapidapi.com/lookup"
UTELLY_HEADERS = {'x-rapidapi-host': "utelly-tv-shows-and-movies-availability-v1.p.rapidapi.com",'x-rapidapi-key': "6f9401aad4msh44554d944610128p148132jsn9766e57a2be6"}
# JESSICA STERN EMAIL KEY = "1143a34b31msh6b1412e3803f9dcp1221cfjsn5ea4ee0dfb85"
# JESSICA PERSONAL EMAIL 2 KEY: "6f9401aad4msh44554d944610128p148132jsn9766e57a2be6"
# KITTY KEY 1 = "e9bbb712c8msh12658873185a8a4p12aea1jsn7e5f6edc1117"
HULU_PRICE = 5.99
NETFLIX_PRICE = 8.99
AMAZON_PRICE = 8.99
HBO_PRICE = 14.99
# above from Jessica 04.20

############################### METHODS ###############################
'''
WEB SCRAPE: Finds prices on Google Play to rent or buy content

Input: string url - url returned by Utelly of where find content
Returns: float rent_money, float buy_money
        Sometimes Google lies and doesn't have any purchase option - returns False

Created by Kitty, modified by Jessica - 04.20

NOTE: please do not write methods starting with a capital letter
NOTE: NOT GETTING PRICES FOR PURCHASING ALL SEASONS
'''
def googlePlay(url):
    # sets up webscrape
    page = requests.get(url)
    bs = BeautifulSoup(page.text, 'html.parser')
    
    # webscrape for price listings
    price_loc = bs.findAll('span','oocvOe')
    rent_str = ""
    buy_str = ""
    if len(price_loc) > 1:
        # if have rent and buy option
        rent_str = price_loc[0].text
        buy_str = price_loc[1].text
    elif len(price_loc) == 1:
        # if only have buy option
        buy_str = price_loc[0].text
    else:
        return False
    
    # parse price listings
    # creating default empty rent_money in case no rent option
    rent_money = rent_str[1:rent_str.find(' ')]
    if rent_money == "":
        rent_money = "0.0"
    buy_money = buy_str[1:buy_str.find(' ')]
    
    return float(rent_money), float(buy_money)

'''
WEB SCRAPE: Finds prices on iTunes to rent or buy content

Input: string url - url returned by Utelly of where find content
Returns: float rent_money, float buy_money
NOTE: NOT ACCOUNTING FOR WHEN CAN ONLY BUY EPISODES ONE BY ONE INSTEAD OF BY SEASON
    - Returns False

Created by Kitty, modified by Jessica - 04.20

NOTE: please do not write methods starting with a capital letter
NOTE: NOT GETTING PRICES FOR PURCHASING ALL SEASONS
'''
def itunes(url):
    # set up webscrape
    page = requests.get(url)
    bs = BeautifulSoup(page.text, 'html.parser')
    
    # webscrape for price listings
    price_loc = bs.findAll('li','inline-list__item inline-list__item--slashed')
    # see note about cases where can't purchase by season; will want to patch later
    if len(price_loc) == 0: 
        return False
    rent_str = ""
    buy_str = ""
    # NOTE: HAVE TO MAKE ASSUMPTIONS THAT RENTING AND BUYING NEVER SAME PRICE
    if price_loc[0].text.strip() != price_loc[1].text.strip():
        # if have rent option
        rent_str = price_loc[0].text.strip()
        buy_str = price_loc[1].text.strip()
    else:
        buy_str = price_loc[0].text.strip()
    
    # parse price listings
    rent_money = rent_str[rent_str.find('$')+1:]
    # if didn't have rent option
    if rent_money == "":
        rent_money = "0.0"
    buy_money = buy_str[buy_str.find('$')+1:] 
    
    return float(rent_money), float(buy_money)

'''
Finds prices on Amazon Instant Videos to rent or buy content

Input: string url - url returned by Utelly of where find content
Returns: float rent_money, float buy_money

Created and modified by Jessica - 04.20

NOTE: NOT USING FOR NOW, BUT WILL KEEP INFRASTRUCTURE IN CASE LOAD BACK IN LATER
'''
def amazonInstant(url):
    # LEAVING THIS BLANK RIGHT NOW, WILL COME BACK LATER IF POSSIBLE
    return 0.0, 0.0


'''
UTELLY API: Extract locations from Utelly result location dictionary 
for one piece of content.

Input: list locations
Returns: dictionary of prices and locations

Created and modified by Jessica from Kitty's content - 4.20
'''
def utelly_parse_locations(locations):
    # will be returning nested dictionary
        # first level split by individual purchase and flatrate plan
        # second level split by platform
        # platform holding tuples or boolean for each movie
    toReturn = {'individual':{'google':(0.0,0.0), 'itunes':(0.0,0.0), 'amazon instant':(0.0,0.0)},
                'subscription':{'amazon prime':False, 'hbo':False, 'netflix':False, 'hulu':False}}
    
    # Go into each location dictionary
    # COME BACK LATER, THIS SHOULD HONESTLY BE A SWITCH-CASE SET UP
    # NOTE: SOME LESS ITEMS CAN SLIP THROUGH THE CRACKS IF SCRAPES AND COLLECTIONS CAN'T GET INFO
    for loc in locations:
        if loc['display_name'] == "Google Play":
            toGoogle = googlePlay(loc['url'])
            if toGoogle is not False:
                toReturn['individual']['google'] = toGoogle
        elif loc['display_name'] == "iTunes":
            toItunes = itunes(loc['url'])
            if toItunes is not False:
                toReturn['individual']['itunes'] = toItunes
        elif loc['display_name'] == "Amazon Instant Video":
            toReturn['individual']['amazon instant'] = amazonInstant(loc['url'])
        elif loc['display_name'] == "Amazon Prime Video":
            toReturn['subscription']['amazon prime'] = True
        elif loc['display_name'] == "HBO":
            toReturn['subscription']['hbo'] = True
        elif loc['display_name'] == "Netflix":
            toReturn['subscription']['netflix'] = True
        elif loc['display_name'] == "Hulu":
            toReturn['subscription']['hulu'] = True
    
    return toReturn


''' 
UTELLY API: For content title (object converted to string) call Utelly API 
for information returned as json file. Parse information and return as list.

Input: string title, string imdb_id
Returns: if Utelly finds content - dictionary of location presence and prices; 
         if Utelly can't find content - returns False

Created and modified by Jessica from content written by Kitty - 04.20
'''
def call_Utelly(title, imdb_id):
    # calling Utelly for one item
    query = {"term": title, "country":"us"} 
    # eventually may want geolocate ability to modify country argument of query
    resp = requests.get(url=UTELLY_URL, headers=UTELLY_HEADERS, params=query).json()
    
    for result in resp['results']:
        # checking that utelly found our query
        # matching against IMDb id ('Const' column) 
            # CONVERT THIS TO ID ENDPOINT LATER?
        if result['external_ids']['imdb'] is not None:
            if result['external_ids']['imdb']['id'] == imdb_id:
                # found query, find locations
                locReturn = utelly_parse_locations(result['locations']) 
                return locReturn

    return False

'''
UTELLY API: Takes in fresh watchlist and processes content through Utelly. 
Gathers all locations of content on watchlist. Also includes information 
on prices for individual purchases.

Input: pandas.Dataframe watchlist - titles column of watchlist
       NOTE: AS LONG AS WATCHLIST HAS A COLUMN CALLED ['Title'] THAT'S CONTENT TITLES
             AND A COLUMN CALLED ['Const'] THAT'S IMDb IDS, ANY DATAFRAME IS GOOD
       NOTE: call from db_connect.fetch_watchlist(watchlist_table_name)
Returns: dictionary parsed_loc - dictionary containing lists of content 
                                 from watchlist at each location

Created and modified by Jessica from content written by Kitty - 04.20
NOTE: JESSICA 05.01 - need to add google_url and itunes_url
'''
def watchlist_parse(watchlist):
    # dictionaries containing lists of items available on each platform
    parsed_loc = {'ids':{},
                'individual':{'google':{'rent':dict(),'buy':dict()},
                              'itunes':{'rent':dict(),'buy':dict()},
                              'amazon instant':{'rent':dict(),'buy':dict()}},
                'subscription':{'amazon prime':[],
                                'netflix':[],
                                'hbo':[],
                                'hulu':[]},
                'nowhere':[]}
    
    # Print to track completion progress and where bugs happen
    print("Beginning watchlist parse:")
    # iteration through titles on watchlist
    for index, row in watchlist.iterrows():
        title = row['Title']
        imdb_id = row['Const']
        
        # Print to track completion and bugs
        print(index,":",title)
        
        # API CALL
        title_location = call_Utelly(title, imdb_id)

        # track imdb_id as unique identifier joining sql tables together
        parsed_loc['ids'][title]= imdb_id
        
        if title_location is False:
            # Can't find content on any major platforms
            parsed_loc['nowhere'].append(title)
        else:
            # parsing individual purchases - key = title; values = tuple(price, url)
            # GOOGLE
            if title_location['individual']['google'][0] != 0.0:
                # rent option
                parsed_loc['individual']['google']['rent'][title] =  title_location['individual']['google'][0]
            if title_location['individual']['google'][1] != 0.0:
                # buy option
                parsed_loc['individual']['google']['buy'][title] = title_location['individual']['google'][1]
                                                                 
            # ITUNES
            if title_location['individual']['itunes'][0] != 0.0:
                # rent option
                parsed_loc['individual']['itunes']['rent'][title] = title_location['individual']['itunes'][0]
            if title_location['individual']['itunes'][1] != 0.0:
                # buy option
                parsed_loc['individual']['itunes']['buy'][title] = title_location['individual']['itunes'][1]
            # AMAZON INSTANT
            # NOTE: NOT IMPLEMENTING YET, WHEN FIGURE OUT HOW FIND PRICES, ADD IN
            
                                                                 
            # parsing subscriptions
            # AMAZON PRIME
            if title_location['subscription']['amazon prime'] is True:
                parsed_loc['subscription']['amazon prime'].append(title)
            # NETFLIX
            if title_location['subscription']['netflix'] is True:
                parsed_loc['subscription']['netflix'].append(title)
            # HBO
            if title_location['subscription']['hbo'] is True:
                parsed_loc['subscription']['hbo'].append(title)
            # HULU
            if title_location['subscription']['hulu'] is True:
                parsed_loc['subscription']['hulu'].append(title)
        # end for loop
    return parsed_loc

'''
Compare rent prices for content acquired individually.
One piece of content at a time for where can get best rent price,
only if can't already get content through subscription

Input: string content, dictionary inds (from parsed_watchlist['individual'])
Returns: string platform, float price
         If something fails in comparison, returns False

Created and modified by Jessica from content written by Kitty - 04.20
'''
def compare_ind_rent(content, inds):
    # create variables to compare
    google_rent = 0.0
    itunes_rent = 0.0
    
    # find values of variables comparing
    if content in inds['google']['rent']: 
        google_rent = float(inds['google']['rent'][content])
    if content in inds['itunes']['rent']: 
        itunes_rent = float(inds['itunes']['rent'][content])
        
    # compare values
    if google_rent > itunes_rent and itunes_rent != 0.0:
        return ('iTunes', itunes_rent)
    elif google_rent != 0.0:
        return ('Google Play', google_rent)
    
    return False

'''
Compare buy prices for content acquired individually.
One piece of content at a time for where can get best buy price,
only if can't already get content through subscription

Input: string content, dictionary inds (from parsed_watchlist['individual'])
Returns: string platform, float price
         If something fails in comparison, returns False

Created and modified by Jessica from content written by Kitty - 04.20
'''
def compare_ind_buy(content, inds):
    # create variables to compare
    google_buy = 0.0
    itunes_buy = 0.0
    
    # find values of variables comparing
    if content in inds['google']['buy']: 
        google_buy = float(inds['google']['buy'][content])
    if content in inds['itunes']['buy']: 
        itunes_buy = float(inds['itunes']['buy'][content])
        
    # compare values
    if google_buy > itunes_buy and itunes_buy != 0.0:
        return ('iTunes', itunes_buy)
    elif google_buy != 0.0:
        return ('Google Play', google_buy)
    
    return False

'''
Compare prices for content acquired individually.
One piece of content at a time for where can get best price,
only if can't already get content through subscription

Input: string content, dictionary inds (from parsed_watchlist['individual'])
Returns: string platform, float price

Created and modified by Jessica from content written by Kitty - 04.20
Modified by Jessica: catching False returns - 04.21
'''
def compare_individual(content, inds):
    # compare rent prices
    best_rent = compare_ind_rent(content, inds)
    
    # compare buy prices
    best_buy = compare_ind_buy(content, inds)
    
    # returned variable
    best_inds = dict()
    if best_rent is not False:
        best_inds['rent'] = {'platform':best_rent[0],'price':best_rent[1]}
    if best_buy is not False:
        best_inds['buy'] = {'platform':best_buy[0],'price':best_buy[1]}
    return best_inds

'''
Compare flatrate subscriptions.
Lists of content at a time.

Input: dictionary subscriptions
Returns: If there's content using platforms - string platform, float price
         If there's no content using platforms - boolean False

Created and modified by Jessica from content written by Kitty - 04.20
'''
def compare_subscriptions(subscriptions):
    # variables to track platform with best price to content ratio
    best_plat = ''
    
    # NOTE: NOT USING LENGTH OF CONTENT YET
    # NOTE: NOT PROPERLY WEIGHING TV SHOW AGAINST MOVIES
    
    # NOTE: SIMPLISTIC COMPARISON OF MONTHLY RATE/# ITEMS FOUND ON PLATFORM
    # dictionary of price per item
    calc_price = {'amazon prime':0.0, 'netflix':0.0, 'hbo':0.0, 'hulu':0.0}
    
    # calculating values
    # AMAZON PRIME
    if len(subscriptions['amazon prime']) > 0:
        calc_price['amazon prime'] = AMAZON_PRICE/len(subscriptions['amazon prime'])
        if best_plat == '':
            best_plat = 'amazon prime'
        else:
            if calc_price['amazon prime'] < calc_price[best_plat]:
                best_plat = 'amazon prime'
    # NETFLIX
    if len(subscriptions['netflix']) > 0:
        calc_price['netflix'] = NETFLIX_PRICE/len(subscriptions['netflix'])
        if best_plat == '':
            best_plat = 'netflix'
        else:
            if calc_price['netflix'] < calc_price[best_plat]:
                best_plat = 'netflix'
    # HBO
    if len(subscriptions['hbo']) > 0:
        calc_price['hbo'] = HBO_PRICE/len(subscriptions['hbo'])
        if best_plat == '':
            best_plat = 'hbo'
        else:
            if calc_price['hbo'] < calc_price[best_plat]:
                best_plat = 'hbo'
    # HULU
    if len(subscriptions['hulu']) > 0:
        calc_price['hulu'] = HULU_PRICE/len(subscriptions['hulu'])
        if best_plat == '':
            best_plat = 'hulu'
        else:
            if calc_price['hulu'] < calc_price[best_plat]:
                best_plat = 'hulu'
    
    if best_plat == 'amazon prime': 
        return 'Amazon Prime Video', AMAZON_PRICE
    elif best_plat == 'netflix':
        return 'Netflix', NETFLIX_PRICE
    elif best_plat == 'hbo':
        return 'HBO', HBO_PRICE
    elif best_plat == 'hulu':
        return 'Hulu', HULU_PRICE
    return False

'''
Generate set of content accessable through subscription platforms.

Input: dictionary subscriptions
Returns: set in_subs

Created by Jessica - 04.20
'''
def subscript_set(subscriptions):
    in_subs = set()
    for key in subscriptions.keys():
        for cont in subscriptions[key]:
            in_subs.add(cont['title'])
        # in_subs.update(subscriptions[key])
    return in_subs

'''
Generate set of content accessable through individual transactions.

Input: dictionary individual
Returns: set ind_set

Created by Jessica - 04.21
'''
def indiv_allset(individual):
    ind_set = set()
    for item in individual['google']['buy'].keys():
        ind_set.add(item)
    for item in individual['itunes']['buy'].keys():
        ind_set.add(item)
    return ind_set

'''
Generate set of content accessed individual and not through subscriptions.

Input: dictionary parsed_watch
Returns: set ind_set

Created by Jessica - 04.20
'''
def indiv_subset(parsed_watch):
    in_subs = subscript_set(parsed_watch['subscription'])
    ind_set = set()
    for item in parsed_watch['individual']['google']['buy'].keys():
        if item not in in_subs:
            ind_set.add(item)
    for item in parsed_watch['individual']['itunes']['buy'].keys():
        if item not in in_subs:
            ind_set.add(item)
    return ind_set

'''
UTELLY API: Generates recommendation for watchlist for subscription and individual.
DO NOT USE ANYMORE: RETAINING SINCE CAN RUN RECOMMENDATION FROM SCRATCH

Input: pandas.Dataframe watchlist
Returns: dictionary reccs

Created and modified by Jessica from content written by Kitty - 04.20
'''
def platform_recommend_API(watchlist):
    # dictionary to return 
        # tuple of best platform
        # dictionaries for content have to get individually
    reccs = {'subscription':(),
             'individual':dict()}
    
    # parsing locations and prices
    locPrice = watchlist_parse(watchlist)
    
    # finding best subscription platform
    subscript_loc = locPrice['subscription']
    reccs['subscription'] = compare_subscriptions(subscript_loc)
    
    # finding which content not available through the flatrate platforms
    in_subs = subscript_set(locPrice['subscription'])
    individual_set = indiv_subset(locPrice)
    
    # generate list of recommendations for what can't be acquired through subscriptions
    for content in individual_set:
        reccs['individual'][content] = compare_individual(content, locPrice['individual'])
     
    return reccs

'''
MySQL: Generates recommendation for watchlist for subscription and individual.

Input: dictionary locPrice - precreated parshed watchlist
Returns: dictionary reccs

Created and modified by Jessica from content written by Kitty - 04.20
'''
def platform_recommend_SQL(locPrice):
    # print("LocPrice:\n" + str(locPrice) + "\n\n\n")
    # dictionary to return 
        # tuple of best platform
        # dictionaries for content have to get individually
    reccs = {'subscription':(),
             'individual':dict()}
    
    # finding best subscription platform
    subscript_loc = locPrice['subscription']
    reccs['subscription'] = compare_subscriptions(locPrice['subscription'])
    
    # finding which content not available through the flatrate platforms
    in_subs = subscript_set(locPrice['subscription'])
    individual_set = indiv_subset(locPrice)
    
    # generate list of recommendations for what can't be acquired through subscriptions
    for content in individual_set:
        # print(content)
        reccs['individual'][content] = compare_individual(content, locPrice['individual'])
     
    return reccs


# NOTE: WRITE UPDATE METHODS FOR SQL


# POTENTIAL UPGRADE: WEIGH TV SHOWS HEAVIER THAN MOVIES
# POTENTIAL UPGRADE: WEIGH USER GENRE PREFERENCES
# POTENTIAL UPGRADE: USER RANK PRIORITY OF LIST? - MAJOR UPGRADE TO SITE OVERALL





