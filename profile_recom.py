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
import poster_image as pi
# import db_connect as db_conn

# import requests
# import pandas as pd
# above from Jessica 04.20

############################### CLASSES ###############################


############################### METHODS ###############################

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
    # print(individual)
    
    # iterating through individual
    for title in individual:
        if 'buy' in individual[title]:
            indiv_buys.append({'title':title,
                                'platform':individual[title]['buy']['platform'],
                                'price':individual[title]['buy']['price']})
    return indiv_buys

'''
Main method of file creating final output heading towards webserver

Input: string username: unique to each user
       string template - name of html template file - Jessica 04.27 remove
       string table_name - LINK TO USER IDENTIFICATION - Jessica 04.30
Returns: dictionary template_inputs: what would be needed to render template
    renders html template - Jessica 04.27 remove

Created by Jessica 04.21
'''
def main(username):    
    # call content from sql
    # CHANGE TO USERNAME
    parsed_loc = cs.retrieve_from_sql(username)
    
    # generate recommendations
    recommends = sr.platform_recommend_SQL(parsed_loc)
    # print(recommends)

    # recommendation for streaming service
    service_recc = recommends['subscription'][0]
    # content from service_recc that can be used -> max four items
    plat_examples = []
    if service_recc == "Amazon Prime Video":
        for item in parsed_loc['subscription']['amazon prime']:
            if len(plat_examples) == 4: break
            plat_examples.append({'title':item['title'], 'poster_url':pi.get_poster_url_sql(item['imdbID'],item['title'])})
    elif service_recc == "Netflix":
        for item in parsed_loc['subscription']['netflix']:
            if len(plat_examples) == 4: break
            plat_examples.append({'title':item['title'], 'poster_url':pi.get_poster_url_sql(item['imdbID'],item['title'])})
    elif service_recc == "HBO":
        for item in parsed_loc['subscription']['hbo']:
            if len(plat_examples) == 4: break
            plat_examples.append({'title':item['title'], 'poster_url':pi.get_poster_url_sql(item['imdbID'],item['title'])})
    elif service_recc == "Hulu":
        for item in parsed_loc['subscription']['hulu']:
            if len(plat_examples) == 4: break
            plat_examples.append({'title':item['title'], 'poster_url':pi.get_poster_url_sql(item['imdbID'],item['title'])})

    # recommendations for individual rent
    indiv_rents = compile_rent(recommends['individual'])

    # recommendations for individual buy
    indiv_buys = compile_buy(recommends['individual'])
    
    # constructing dictionary to return
    template_inputs = {'service_recc':service_recc, 'indiv_rents':indiv_rents, 'indiv_buys':indiv_buys, 'plat_content':plat_examples}
    return template_inputs
