'''
Retrieves watchlist information from SQL and generates recommendation 
page out of information.

NOTE: writing information into SQL will be from watchlist uploading end

Created by Jessica - 04.21
'''
############################### IMPORTS ###############################
from sqlalchemy import create_engine
from flask import Flask, render_template

import service_recc as sr
import convert_sql as cs
# import db_connect as db_conn

# import requests
# import pandas as pd
# above from Jessica 04.20

#######################################################################################

'''
Compile rent recommendations of individually acquired items

Input: dictionary individual
Returns: list indiv_rents

Created by Jessica 04.21
'''
def compile_rent(individual):
    # construct variable to return, will contain dictionaries
        # each dictionary in form: {'title','platform','price'}
    indiv_rents = []
    
    # iterating through individual
    for title in individual:
        if 'rent' in individual[title]:
            indiv_rents.append({'title':title,
                                'platform':individual[title]['rent']['platform'],
                                'price':individual[title]['rent']['price']})
    return indiv_rents

'''
Compile buy recommendations of individually acquired items

Input: dictionary individual
Returns: list indiv_buys

Created by Jessica 04.21

NOTE: COME BACK LATER AND EVALUATE THIS AND ABOVE METHOD FOR SPEED EFFECIENCY
      COMBINE TRAVERSE THROUGH INDIVIDUAL
'''
def compile_buy(individual):
    # construct variable to return, will contain dictionaries
        # each dictionary in form: {'title','platform','price'}
    indiv_buys = []
    
    # iterating through individual
    for title in individual:
        if 'buy' in individual[title]:
            indiv_buys.append({'title':title,
                                'platform':individual[title]['buy']['platform'],
                                'price':individual[title]['buy']['price']})
    return indiv_buys

'''
Main method of file creating final output heading towards webserver

Input: string template - name of html template file
       string table_name - LINK TO USER IDENTIFICATION
Returns: renders html template

Created by Jessica 04.21
'''
def main(template, table_name):
    # VARIABLES TO PASS THROUGH TEMPLATE
    # USER CUSTOMIZED SIDEBAR:
        # User name
        # Join date?
        # User image
        # Sidebar head image   
        # FOR PROTOTYPE, USING DEFAULTS IN TEMPLATE, CHANGE IN FULL PRODUCT
    # RECOMMENDATION CONTENT
        # title of page: "Recommendation" 
        # Streaming service recommendation
            # Potentially a block of up to ten-fifteen movie 
            # posters of what can watch on site from watchlist
        # List of stuff found individually 
            # Some sort of button to toggle between rent and buy
            # Some sort of drop-down menu?
            # Long scroll of what content from where?
    
    # call content from sql
    parsed_loc = cs.retrieve_from_sql(table_name)
    # print(parsed_loc)
    # generate recommendations
    recommends = sr.platform_recommend_SQL(parsed_loc)
    # print(recommends)
    
    # recommendation for streaming service
    service_recc = recommends['subscription'][0]
    # recommendations for individual rent
    indiv_rents = compile_rent(recommends['individual'])
    # recommendations for individual buy
    indiv_buys = compile_buy(recommends['individual'])
    
    return render_template(template,
                           service_recc=service_recc,
                           indiv_rents=indiv_rents,
                           indiv_buys=indiv_buys)
