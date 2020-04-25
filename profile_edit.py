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
	conn.commit()

	return

# @app.route('/profile/edit/bio', methods=('GET','POST'))
# def update_bio(username):
# 	bio = get_bio(username)

# 	if request.method == 'POST':
# 		bio_body = request.form['bio_body']
# 		error = None

# 		update_sql_bio(username, bio_body)
# 		return redirect(url_for('/profile'))

# 	return render_template('profile/profile-edit-bio.html', bio=bio)

'''
Main method rendering profile-edit.html template

Inputs:string template - name of html template file
	   string username - unique value to locate user info
Returns: render_template() of user's "Edit Profile" page

Created by Jessica - 04.25
'''
def main(template, username):
	bio = get_bio(username)

	print()

	return render_template(template, bio=bio)