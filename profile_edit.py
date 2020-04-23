'''
Sets up profile's "Edit Profile" page

Created by Jessica - 04.22
'''
############################### IMPORTS ###############################
from sqlalchemy import create_engine
from flask import Flask, render_template

import service_recc as sr
import convert_sql as cs

############################### GLOBAL VARIABLES ###############################
CONN_STRING = 'mysql+pymysql://{user}:{password}@{host}/{db}?charset={encoding}'.format(
        host = '35.245.115.59', 
        user = 'root',
        db = 'streamline',
        password = 'dwdstudent2015',
        encoding = 'utf8mb4')

#######################################################################################

'''
Retrieve's user bio information

'''


'''
Main method rendering profile-generic.html template

Inputs:string template - name of html template file
       string table_name - LINK TO USER IDENTIFICATION
Returns: render_template() of user's "Edit Profile" page

Created by Jessica - 04.22
'''
def main(template, table_name):
	print()