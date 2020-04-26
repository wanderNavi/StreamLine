from flask import Flask, render_template, request
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
import db_connect as db_conn

def main():
    con = db_conn.get_db()

    ret = render_template('bootstrap_login-login.html')
    return ret

# Need function to get data user submits and compare it to SQL database
# If okay, direct to profile page