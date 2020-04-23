from flask import Flask, render_template, request
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from datetime import datetime

def get_time():
    datetime.now().strftime('%Y-%m-%d %H:%M:%S') #converts datetime to string, but shouldn't we switch back so that we can sort join_date in SQL by recent to oldest?
    date = datetime.now().strftime('%Y-%m-%d')
    time = datetime.now().strftime('%H:%M:%S')
    return date + time

def test():
    username = str(request.args.get('username'))
    password = str(request.args.get('pass'))
    conn_string = 'mysql+pymysql://{user}:{password}@{host}/{db}?charset={encoding}'.format(
        host = '35.245.115.59:3306', 
        user = 'root',
        db = 'streamline',
        password = 'dwdstudent2015',
        encoding = 'utf8mb4')
    engine = create_engine(conn_string)
    con = engine.connect()
    test_query = '''SELECT username FROM all_user_data WHERE EXISTS (SELECT username FROM all_user_data WHERE username = {username}'''.format(username=username)
    con.execute(test_query)
    return test_query
    
def main():
    if test() == True:
        # pop up message on sign up screen
        message = "You already have an existing account. Please return to Login."
        ret = render_template('bootstrap-login-signup.html', message=message)
    else:
        username = str(request.args.get('username'))
        password = str(request.args.get('pass'))
        fname = str(request.args.get('first'))
        lname = str(request.args.get('last'))
        email = str(request.args.get('email'))
        join_date = get_time()
        message = "Success! Thank you for joining StreamLine."
        query_template = '''INSERT IGNORE INTO {db}.{table}(username, 
                                        password, 
                                        fname,
                                        lname,
                                        email,
                                        join_date) 
                    VALUES (%s, %s, %s, %s, %s, %s)'''.format(db='streamline', table='all_user_data')
        con.execute(query_template, query_parameters)
        ret=render_template('bootstrap-login-signup.html',page_title="Success!",message=message)
    con.close()
    return ret
    

