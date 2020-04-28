'''
Controls sign up systems
'''
############################### IMPORTS ###############################
from flask import Flask, render_template, request
from sqlalchemy import MetaData, Table, Column, Integer, String
from datetime import datetime

import db_connect as dbc

############################### METHODS ###############################
def get_time():
    datetime.now().strftime('%Y-%m-%d %H:%M:%S') #converts datetime to string, but shouldn't we switch back so that we can sort join_date in SQL by recent to oldest? # Jessica: That's not a problem?
    date = datetime.now().strftime('%Y-%m-%d')
    time = datetime.now().strftime('%H:%M:%S')
    return date + " " + time

'''
Checks if username is already in our database and hence user account already exists/claimed
NOTE: WEBSERVER.PY BYPASSES THIS METHOD CHECK. SEE NOTES BELOW. 

Inputs:
Returns: boolean True if user already in database
         boolean False if user not already in database

Created by Jenny
Modified by Jessica - 04.27:
    Correct query
    Create method description
    Corret return
'''
def test():
    # connect to database 
    con = dbc.get_db()

    # get user provided username and password
    username = str(request.args.get('username'))
    password = str(request.args.get('pass'))

    # query check if user already exists
    test_query = '''SELECT EXISTS(SELECT * FROM all_user_data WHERE username="{username}")'''.format(username=username)
    # BELOW CAUSING ERROR
    # test_query = '''SELECT username FROM all_user_data WHERE EXISTS (SELECT username FROM all_user_data WHERE username = {username}'''.format(username=username)
    test_check = con.execute(test_query)
    con.close()
    # parse through returned object
    for ent in test_check:
        if ent[0] == 1:
            return True
    return False
    
'''
Main method to generate what needed to render templates
NOTE: ACTUALLY DOING MOST IN WEBSERVER.PY ITSELF, TURNS OUT THAT SINCE WE HAVEN'T SET UP APPROPRIATE APPLICATION AND BLUEPRINT FILES, IT'S EASIEST TO JUST WRITE WHAT WE NEED IN THERE :| 
THIS VERSION DOES NOT HANDLE ERRORS AND METHODS POST WELL - Jessica 04.27

Inputs:
Returns:

Created by Jenny
Modified by Jessica - 04.27:
    Cleaned up some errors being created 
'''
def main():
    con = dbc.get_db()
    if test() == True:
        # pop up message on sign up screen
        message = "You already have an existing account. Please return to Login."
        ret = render_template('bootstrap-login-signup.html', message=message)
    else:
        # NEED TO CATCH WHERE HAVE 'NONE' IN ALL FIELDS
        username = str(request.args.get('username'))
        password = str(request.args.get('pass'))
        fname = str(request.args.get('first'))
        lname = str(request.args.get('last'))
        email = str(request.args.get('email'))
        join_date = get_time()
        query_parameters = (username, password, fname, lname, email, join_date)
        message = "Success! Thank you for joining StreamLine."

        query_template = '''INSERT IGNORE INTO {db}.{table}(username, 
                                        password, 
                                        fname,
                                        lname,
                                        email,
                                        join_date) 
                    VALUES (%s, %s, %s, %s, %s, %s)'''.format(db='streamline', table='all_user_data')
        # con.execute(query_template, query_parameters)
        ret=render_template('bootstrap-login-signup.html',page_title="Success!",message=message)
    con.close()
    return ret
    

