'''
Sets up profile's "Edit Profile" page

Created by Jessica - 04.22
'''
############################### IMPORTS ###############################
from sqlalchemy import create_engine
from flask import Flask, render_template

import service_recc as sr
import convert_sql as cs
import db_connect as db_conn

#######################################################################################

'''
Retrieve's user bio information

Inputs:
Returns:

Created by Jessica - 04.22
'''
def retrieve_bio():
	# filler text for now
	filler = "Has a cat and a dog and likes to take long walks on the beach."
	# NOTE: NEED TO CREATE COLUMN FOR THIS 
	print()

'''
Main method rendering profile-generic.html template

Inputs:string template - name of html template file
       string table_name - LINK TO USER IDENTIFICATION
Returns: render_template() of user's "Edit Profile" page

Created by Jessica - 04.22
'''
def main(template, table_name):
	print()