'''
Connects with TMDb and gets their poster images. 
Going to figure out how to use their logo later to complete the appropriate attribution requests. 

Created by Jessica - 04.26
'''
########### IMPORTS ###########
import requests

import db_connect as db

########### GLOBAL VARIABLE ###########
POSTER_URL_HEAD = "http://image.tmdb.org/t/p/w185"
NO_POSTER_URL = "https://media.discordapp.net/attachments/662866911348129823/704170526263869450/image0.png"

########### METHODS ###########
'''
Connects to TMDb using my API key

Inputs: string external_id: IMDb ID for content
Returns: dictionary cont_response: returned response from pinging the API

Created by Jessica - 04.26
'''
def single_content_TMDb(external_id):
	TMDb_url = 'https://api.themoviedb.org/3/find/'+external_id
	TMDb_param = {
		'api_key': '5eac2ee68ef7e4aaa0413bdfedc574d5',
		'external_source': 'imdb_id'
	}
	cont_response = requests.get(TMDb_url, params=TMDb_param)
	return cont_response.json()

'''
Extract poster url from TMDb response
Build url on: "http://image.tmdb.org/t/p/w150"
If poster_path is not Null: single_content_TMDb()['movie_results'][0]['poster_path'] or ['tv_results'][0]['poster_path']
If don't have url, use: "https://media.discordapp.net/attachments/662866911348129823/704170526263869450/image0.png"

Inputs: string external_id: IMDb ID of content
Returns: string image_url

Created by Jessica - 04.26
'''
def get_poster_url(external_id):
	# call API
	TMDb_response = single_content_TMDb(external_id)

	# technically could push bottom two into separate methods in case grab content type info out of downloaded watchlist's columns
	# if content is movie
	if len(TMDb_response['movie_results']) == 1:
		if TMDb_response['movie_results'][0]['poster_path'] != None:
			return POSTER_URL_HEAD+TMDb_response['movie_results'][0]['poster_path']

	# if content is tv show
	if len(TMDb_response['tv_results']) == 1:
		if TMDb_response['tv_results'][0]['poster_path'] != None:
			return POSTER_URL_HEAD+TMDb_response['tv_results'][0]['poster_path']

	return NO_POSTER_URL

'''
Retrieve url from database. 
If not in database, puts url into database.
Don't want to keep asking the API each time the user refreshes the page.

Inputs: string external_id: IMDb id of content
		string tile: name of content from IMDb watchlist
Returns: string url: image url to use in displaying poster

Created by Jessica - 04.26
'''
def get_poster_url_sql(external_id, title):
	# connect to database
	con = db.get_db()

	# does entry already exist?
	exist_query = '''SELECT EXISTS(SELECT * FROM posters WHERE imdbID="{id}")'''.format(id=external_id)
	exist_check = con.execute(exist_query)

	for ent in exist_check:
		if ent[0] == 1: # does already exist
			# check if doesn't have poster
			retrieve_query = '''SELECT * FROM posters WHERE imdbID="{id}"'''.format(id=external_id)
			retrieve_url = con.execute(retrieve_query)
			# THERE HAS TO BE A BETTER WAY TO DO THIS
			image_url = ''
			for ret in retrieve_url:
				image_url = ret[2]
			if image_url == NO_POSTER_URL:
				replace_url = get_poster_url(external_id)
				insert_query = '''UPDATE posters SET url="{url}" WHERE imdbID="{id}"'''.format(url=replace_url, id=external_id)
				con.execute(insert_query)
				con.close()
				return replace_url
			else:
				con.close()
				return image_url
		else: # does not already exist
			replace_url = get_poster_url(external_id)
			insert_query = '''INSERT INTO posters (imdbID, title, url) VALUES ("{id}","{title}","{url}")'''.format(id=external_id, title=title, url=replace_url)
			con.execute(insert_query)
			con.close()
			return replace_url

	return NO_POSTER_URL