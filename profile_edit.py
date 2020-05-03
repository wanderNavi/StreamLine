'''
Sets up profile's "Edit Profile" page

Created by Jessica - 04.22
'''
############################### IMPORTS ###############################
from sqlalchemy import create_engine
from flask import Flask, render_template

import service_recc as sr
import convert_sql as cs
import db_connect as db

#######################################################################################
'''
Retrieve user author card information

Inputs: string username - unique to each user in database
Returns: dictionary card - dictionary containing first name, last name, and join month and year
NOTE: WILL NEED TO RETRIEVE PROFILE PHOTO EVENTUALLY

Created by Jessica - 04.28
'''
def get_card(username):
	# connect to database
	conn = db.get_db()

	# create to return dictionary
	card = {'first':'',
			'last':'',
			'month':'',
			'year':''}

	# fetch content from all user table
	user_info = conn.execute('''SELECT * FROM all_user_data WHERE username="{username}"'''.format(username=username)).fetchone()
	conn.close()

	# fill information
	card['fname'] = user_info['fname']
	card['lname'] = user_info['lname']
	card['join_month'] = user_info['join_date'].strftime("%B")
	card['join_year'] = user_info['join_date'].year

	return card

'''
Retrieve's user bio information

Inputs: string username - unique to each user
Returns: string (?) bio information

Created by Jessica - 04.25
'''
def get_bio(username):
	# connect to database
	conn = db.get_db()

	# fetch bio content from all user table
	bio = conn.execute(
		'SELECT user_bio FROM all_user_data WHERE username = %s',
		(username,),
		).fetchone()
	conn.close()

	# check if bio is empty
	if bio[0] is None:
		return ""

	return bio[0]

'''
Editing bio and sending off to database for storage

Inputs: string username
		string bio
Returns:

Created by Jessica - 04.25
'''
def update_sql_bio(username, bio):
	# connect to database
	conn = db.get_db()

	# write new bio content into database
	conn.execute(
		'UPDATE all_user_data SET user_bio = %s WHERE username = %s',
		(bio, username),
		)
	# conn.commit()
	conn.close()
	return

'''
Sure we could use word tokenizers and regex, but what if I just wrote a recussive function to parse this instead

Input: string genres, list parsed
Returns: list tgenres

Created by Jessica - 04.25
'''
def parse_genres_recur(genres, parsed):
	index = genres.find(',')
	if index == -1 and len(genres)>1:
		parsed.append(genres[1:])
		return parsed
	parsed.append(genres[1:index])
	return parse_genres_recur(genres[index+1:], parsed)

'''
Helper method: Set up for the recursion
'''
def parse_genres(genres):
	index = genres.find(',')
	if index == -1:
		return [genres.strip()]
	toRet = [genres[0:index]]
	return parse_genres_recur(genres[index+1:], toRet)

'''
Calculates and returns genre by rank

Inputs: string username
Returns: dictionary ranked 

Created by Jessica - 04.25
'''
def ranked_genre(username):
	# connect to database
	conn = db.get_db()

	# fetch watchlist content
	# CURRENTLY HARDCODE, NEED TO SETUP VARIABLE LATER
		# "IMDb_Watchlist_username"?
	genres = conn.execute('''SELECT Const, Genres FROM IMDb_Watchlist WHERE username="{username}" GROUP BY Const, Genres'''.format(username=username)).fetchall()

	# parse genres in watchlist into dictionary
		# key -> genre
		# value -> incrementing
	genre_dict = {}
	for title in genres:
		tgenres = parse_genres(title['Genres'])
		for ent in tgenres:
			if ent not in genre_dict.keys():
				genre_dict[ent] = 1
			else:
				genre_dict[ent] += 1

	ranked = {k:v for k,v in sorted(genre_dict.items(), key=lambda item:item[1], reverse=True)}
	conn.close()
	return ranked

'''
Returns top three genres and how many titles
Eventually link with method finding example posters?

Inputs: dictionary ranked
Returns: dictionary top_three
'''
def three_genre(ranked):
	top_three = {}
	if len(ranked.keys()) >= 3:
		for i, (k,v) in enumerate(ranked.items()):
			# print(i, k, v)
			top_three[k] = v
			if i == 2: break

	return top_three

'''
Main method rendering profile-edit.html template

Inputs:string template - name of html template file
	   string username - unique value to locate user info
Returns: render_template() of user's "Edit Profile" page

Created by Jessica - 04.25
'''
def main(template, profile):
	bio = get_bio(profile['username'])

	print()

	return render_template(template, profile=profile)