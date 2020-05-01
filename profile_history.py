'''
Sets up profile's "Profile History" page

Created by Jessica - 04.25
'''
############################### IMPORTS ###############################
from sqlalchemy import create_engine
from flask import Flask, render_template
import pandas as pd
import numpy as np

# import service_recc as sr
# import convert_sql as cs
import db_connect as db
import poster_image as pi

#######################################################################################

'''
Get watchlist from database to print out on its page

Inputs: string username: username of user with watchlist - Jessica 04.29 change
		string watchlist_name: user set name of watchlist - Jessica 04.29 change

		string full_watchlist: name of table in database containing full watchlist info (ex: "IMDb_Watchlist_Jenny")
		string parsed_watchlist: name of table in database containing parsed location info for watchlist (ex. "Parsed_Watchlist_Jenny")
	EVENTUALLY: WANT TO JUST TAKE USERID AND USE THAT TO LOCATE RELEVANT WATCHLIST TABLES
Returns: list title_cards: list ordered based on full_watchlist of stuff

Created by Jessica - 04.26
'''
def parse_watchlist_for_page(username, watchlist_name):
	# get dataframe of info combined between full and parsed
	cards_content = db.fetch_html_watchlist(username, watchlist_name)
	# get dataframe of ordered full_watchlist info
	ordered_list = db.fetch_watchlist(username, watchlist_name)
	# list of parsed info each content card - to return
	title_cards = []

	print("\ncards_content:",cards_content)
	print("\nordered_list:",ordered_list)
	print("\nordered_list[Const]:",ordered_list['Const'])

	# iterate through each line of full_watchlist and grab info from cards_content to put into title_cards
	for imdb_id in ordered_list['Const']:
		print("imdb_id:", imdb_id)
		card = {'title':'', 'year':'', 'genres':'', 'rating':'', 'image_url':'',
				'nowhere':'',
				'platform_where':[],
				'indiv':{'where_rent':'','price_rent':'','where_buy':'', 'price_buy':''}}
		# pandas.Series object of info found - consider going about this directly in sql instead later?
		# if 
		card_series = cards_content.loc[imdb_id]
		print("card_series:", card_series)

		# fill in card
		card['title'] = card_series['Title']
		card['year'] = card_series['Year']
		card['genres'] = card_series['Genres'] # MAY WANT TO SPLIT UP IN CASE MAKE IT SO CAN CLICK EACH GENRE TO A LINK IN CONTENT BROWSE
		card['rating'] = card_series['IMDb_Rating']
		card['image_url'] = pi.get_poster_url_sql(imdb_id, card_series['Title'])

		if card_series['nowhere'] == 1:
			card['nowhere'] = True
		else:
			if card_series['amazon_prime'] == 1:
				card['platform_where'].append("Amazon Prime Video")
			if card_series['netflix'] == 1:
				card['platform_where'].append("Netflix")
			if card_series['hbo'] == 1:
				card['platform_where'].append("HBO")
			if card_series['hulu'] == 1:
				card['platform_where'].append("Hulu")

			if np.isnan(card_series['google_rent']) == False and np.isnan(card_series['itunes_rent']) == False:
				if card_series['google_rent'] <= card_series['itunes_rent']:
					card['indiv']['where_rent'] = "Google Play"
					card['indiv']['price_rent'] = card_series['google_rent']
				else:
					card['indiv']['where_rent'] = "iTunes"
					card['indiv']['price_rent'] = card_series['itunes_rent']
			elif np.isnan(card_series['google_rent']) == False and np.isnan(card_series['itunes_rent']) == True:
				card['indiv']['where_rent'] = "Google Play"
				card['indiv']['price_rent'] = card_series['google_rent']
			elif np.isnan(card_series['google_rent']) == True and np.isnan(card_series['itunes_rent']) == False:
				card['indiv']['where_rent'] = "iTunes"
				card['indiv']['price_rent'] = card_series['itunes_rent']
			
			if np.isnan(card_series['google_buy']) == False and np.isnan(card_series['itunes_buy']) == False:
				if card_series['google_buy'] <= card_series['itunes_buy']:
					card['indiv']['where_buy'] = "Google Play"
					card['indiv']['price_buy'] = card_series['google_buy']
				else:
					card['indiv']['where_buy'] = "iTunes"
					card['indiv']['price_buy'] = card_series['itunes_buy']
			elif np.isnan(card_series['google_buy']) == False and np.isnan(card_series['itunes_buy']) == True:
				card['indiv']['where_buy'] = "Google Play"
				card['indiv']['price_buy'] = card_series['google_buy']
			elif np.isnan(card_series['google_buy']) == True and np.isnan(card_series['itunes_buy']) == False:
				card['indiv']['where_buy'] = "iTunes"
				card['indiv']['price_buy'] = card_series['itunes_buy']

		# add card to title_cards
		title_cards.append(card)
	return title_cards