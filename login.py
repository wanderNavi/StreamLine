from flask import Flask, render_template, request
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

def main():
    conn_string = 'mysql+pymysql://{user}:{password}@{host}/{db}?charset={encoding}'.format(
        host = '35.245.115.59:3306', 
        user = 'root',
        db = 'streamline',
        password = 'dwdstudent2015',
        encoding = 'utf8mb4')
    engine = create_engine(conn_string)
    con = engine.connect()
    ret = render_template('bootstrap_login-login.html')
    return ret

# Need function to get data user submits and compare it to SQL database
# If okay, direct to profile page