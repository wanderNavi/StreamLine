##############################################
# This file aims to do web scraping for differnt genres on IMDb website.

# Created by Kitty - 4.30
##############################################
from bs4 import BeautifulSoup
import requests
import numpy as np
import db_connect as db_conn
##############################################

# STILL WORKING ON SUPERHERO URL, DIFFIRENT LAYOUT ON WEBSITE

##############################################
#           FUNCTIONS FOR DATABASE           #

def imdb_database(table_name, index, title, poster, time, certificate, runtime, genre, rate, intro, director, star):
    
    # Connect to database
    con = db_conn.get_db()
    
    # Create a new table
    create_table_query = '''CREATE TABLE IF NOT EXISTS {table} (index varchar(255)
                         title varchar(255), 
                         poster varchar(255),
                         time varchar(255),
                         certificate varchar(255),
                         runtime varchar(255),
                         genre varchar(255),
                         rate real),
                         intro varchar(255),
                         director varchar(255),
                         star varchar(255),
                         PRIMARY KEY(index, title))'''.format(table=table_name)
    con.execute(create_table_query)
    
    # Insert head into the table
    insert_query = '''INSERT IGNORE INTO {table} (index, title, poster, time, certificate, runtime, genre, rate,
                    intro, director, star) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''.format(table=table_name)

    # Execute query
    query_parameters = (index, title, poster, time, certificate, runtime, genre, rate, intro, director, star)
    con.execute(insert_query, query_parameters)
    
    con.close()
    return

'''
This function requires a url as parameter (listed above), and returns the url for the next page for iterative (not include superhero):
    title: str
    poster: str
    time: str
    certificate: str
    runtime: str
    genre: str
    rate: str
    intro: str
    director: str
    star: str
'''
def fetch_imdb(url, table_name):
    
    # Get the web page
    page = requests.get(url)
    bs = BeautifulSoup(page.text, 'html.parser')
    
    # Create dictionary to store the information
    movie_dict = {}
    
    # Fetch the information for the webpage
    movie_list = bs.findAll('div','lister-item mode-advanced')
    
    # Fetch the information for each movie
    for movie in movie_list:
        index = movie.find('span','lister-item-index unbold text-primary').text.strip()
        poster = movie.find('img')['loadlate'].strip() # movie poster        
        title = movie.findAll('a')[1].text.strip() # movie title        
        try:
            time = movie.find('span','lister-item-year text-muted unbold').text.strip().strip() # movie time (published)        
        except:
            time = np.nan
        try:
            certificate = movie.find('span','certificate').text.strip() # movie certificate (R, PG-13,etc.)
        except:
            certificate = np.nan        
        try:
            runtime = movie.find('span','runtime').text.strip() # movie runtime (hours and minutes)
        except:
            runtime = np.nan      
        try:
            genre = movie.find('span','genre').text.strip() # movie genre      
        except:
            genre = np.nan
        try:
            rate = movie.find('div','inline-block ratings-imdb-rating').text.strip() # movie rate (out of 10)
        except:
            rate = np.nan        
        intro = movie.findAll('p','text-muted')[1].text.strip() # movie introduction/description        
        para = movie.findAll('p')[2].text.strip().replace(', ','').split('\n')        
        if '| ' in para:
            director_list = para[1:para.index('| ')] # movie director 
            director = ', '.join(director_list)
            star_list = para[para.index('| ')+2:] # movie star (if contains movie director)
            star = ', '.join(star_list)
        else:
            director = np.nan
            star = para[1:] # movie star (if not contains movie director)
            star = ', '.join(star_list)
        
        # Store the information        
        imdb_database(table_name, index, title, poster, time, certificate, runtime, genre, rate, intro, director, star)

    # Fetch the link for next page
    try:
        next_page = bs.find('a','lister-page-next next-page').get('href')
        next_url = "https://www.imdb.com" + next_page
    except:
        return
    return next_url


'''
This function requires a url as parameter (listed above), and returns the url for the next page for iterative:
    title: str
    poster: str
    time: str
    certificate: str
    runtime: str
    genre: str
    rate: str
    intro: str
    director: str
    star: str
'''
def fetch_superhero_imdb(url, table_name):
    
    # Get the web page
    page = requests.get(url)
    bs = BeautifulSoup(page.text, 'html.parser')
    
    # Create dictionary to store the information
    movie_dict = {}
    
    # Fetch the information for the webpage
    movie_list = bs.findAll('div','lister-item mode-detail')
    
    # Fetch the information for each movie
    for movie in movie_list:
        index = movie.find('span','lister-item-index unbold text-primary').text.strip()
        poster = movie.find('img')['loadlate'].strip() # movie poster        
        title = movie.findAll('a')[1].text.strip() # movie title        
        try:
            time = movie.find('span','lister-item-year text-muted unbold').text.strip().strip() # movie time (published)        
        except:
            time = np.nan  
        try:
            certificate = movie.find('span','certificate').text.strip() # movie certificate (R, PG-13,etc.)
        except:
            certificate = np.nan        
        try:
            runtime = movie.find('span','runtime').text.strip() # movie runtime (hours and minutes)
        except:
            runtime = np.nan        
        try:
            genre = movie.find('span','genre').text.strip() # movie genre     
        except:
            genre = np.nan
        try:
            rate = movie.find('div','inline-block ratings-imdb-rating').text.strip() # movie rate (out of 10)
        except:
            rate = np.nan        
        intro = movie.findAll('p','text-muted')[1].text.strip() # movie introduction/description        
        para = movie.findAll('p')[2].text.strip().replace(', ','').split('\n')        
        if '| ' in para:
            director_list = para[1:para.index('| ')] # movie director 
            director = ', '.join(director_list)
            star_list = para[para.index('| ')+2:] # movie star (if contains movie director)
            star = ', '.join(star_list)
        else:
            director = np.nan
            star = para[1:] # movie star (if not contains movie director)
            star = ', '.join(star_list)
        
        # Store the information      
        imdb_database(table_name, index, title, poster, time, certificate, runtime, genre, rate, intro, director, star)
    
    # Fetch the link for next page
    try:
        next_page = bs.find('a','lister-page-next next-page').get('href')
        next_url = "https://www.imdb.com/search/keyword/" + next_page
    except:
        return
    return next_url



##############################################
#          FUNCTIONS FOR EACH GENRE          #

'''
This function aims to fetch all the comedy movies and related information.
'''
def comedy_imdb():
    # Set the initial url to fetch
    url = "https://www.imdb.com/search/title/?genres=comedy&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=3396781f-d87f-4fac-8694-c56ce6f490fe&pf_rd_r=HS270KKF3EKA0HHP3F0X&pf_rd_s=center-1&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr1_i_1"
    
    # Use loop to fetch all the url page
    while url:
        # Updat the url
        url = fetch_imdb(url,"Comedy_IMDB")
    return


        
'''
This function aims to fetch all the sci-fi movies and related information.
'''
def scifi_imdb():
    # Set the initial url to fetch
    url = "https://www.imdb.com/search/title/?genres=sci-fi&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=3396781f-d87f-4fac-8694-c56ce6f490fe&pf_rd_r=HS270KKF3EKA0HHP3F0X&pf_rd_s=center-1&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr1_i_2"
    # Use loop to fetch all the url page
    while url:
        # Updat the url
        url = fetch_imdb(url,"Scifi_IMDB")
    return


    
'''
This function aims to fetch all the horror movies and related information.
'''
def horror_imdb():
    # Set the initial url to fetch
    url = "https://www.imdb.com/search/title/?genres=horror&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=3396781f-d87f-4fac-8694-c56ce6f490fe&pf_rd_r=HS270KKF3EKA0HHP3F0X&pf_rd_s=center-1&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr1_i_3"
    # Use loop to fetch all the url page
    while url:
        # Updat the url
        url = fetch_imdb(url,"Horror_IMDB")
    return



'''
This function aims to fetch all the romance movies and related information.
'''
def romance_imdb():
    # Set the initial url to fetch
    url = "https://www.imdb.com/search/title/?genres=romance&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=e0da8c98-35e8-4ebd-8e86-e7d39c92730c&pf_rd_r=HS270KKF3EKA0HHP3F0X&pf_rd_s=center-2&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr2_i_1"
    # Use loop to fetch all the url page
    while url:
        # Updat the url
        url = fetch_imdb(url,"Romance_IMDB")
    return



'''
This function aims to fetch all the action movies and related information.
'''
def action_imdb():
    # Set the initial url to fetch
    url = "https://www.imdb.com/search/title/?genres=action&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=e0da8c98-35e8-4ebd-8e86-e7d39c92730c&pf_rd_r=HS270KKF3EKA0HHP3F0X&pf_rd_s=center-2&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr2_i_2"
    # Use loop to fetch all the url page
    while url:
        # Updat the url
        url = fetch_imdb(url,"Action_IMDB")
    return



'''
This function aims to fetch all the thriller movies and related information.
'''
def thriller_imdb():
    # Set the initial url to fetch
    url = "https://www.imdb.com/search/title/?genres=thriller&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=e0da8c98-35e8-4ebd-8e86-e7d39c92730c&pf_rd_r=HS270KKF3EKA0HHP3F0X&pf_rd_s=center-2&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr2_i_3"
    # Use loop to fetch all the url page
    while url:
        # Updat the url
        url = fetch_imdb(url,"Thriller_IMDB")
    return



'''
This function aims to fetch all the drama movies and related information.
'''
def drama_imdb():
    # Set the initial url to fetch
    url = "https://www.imdb.com/search/title/?genres=drama&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=f1cf7b98-03fb-4a83-95f3-d833fdba0471&pf_rd_r=HS270KKF3EKA0HHP3F0X&pf_rd_s=center-3&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr3_i_1"
    # Use loop to fetch all the url page
    while url:
        # Updat the url
        url = fetch_imdb(url,"Drama_IMDB")
    return



'''
This function aims to fetch all the mystery movies and related information.
'''
def mystery_imdb():
    # Set the initial url to fetch
    url = "https://www.imdb.com/search/title/?genres=mystery&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=f1cf7b98-03fb-4a83-95f3-d833fdba0471&pf_rd_r=HS270KKF3EKA0HHP3F0X&pf_rd_s=center-3&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr3_i_2"
    # Use loop to fetch all the url page
    while url:
        # Updat the url
        url = fetch_imdb(url,"Mystery_IMDB")
    return



'''
This function aims to fetch all the crime movies and related information.
'''
def crime_imdb():
    # Set the initial url to fetch
    url = "https://www.imdb.com/search/title/?genres=crime&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=f1cf7b98-03fb-4a83-95f3-d833fdba0471&pf_rd_r=HS270KKF3EKA0HHP3F0X&pf_rd_s=center-3&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr3_i_3"
    # Use loop to fetch all the url page
    while url:
        # Updat the url
        url = fetch_imdb(url,"Crime_IMDB")
    return



'''
This function aims to fetch all the animation movies and related information.
'''
def animation_imdb():
    # Set the initial url to fetch
    url = "https://www.imdb.com/search/title/?genres=animation&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=fd0c0dd4-de47-4168-baa8-239e02fd9ee7&pf_rd_r=HS270KKF3EKA0HHP3F0X&pf_rd_s=center-4&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr4_i_1"
    # Use loop to fetch all the url page
    while url:
        # Updat the url
        url = fetch_imdb(url,"Animation_IMDB")
    return



'''
This function aims to fetch all the adventure movies and related information.
'''
def adventure_imdb():
    # Set the initial url to fetch
    url = "https://www.imdb.com/search/title/?genres=adventure&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=fd0c0dd4-de47-4168-baa8-239e02fd9ee7&pf_rd_r=HS270KKF3EKA0HHP3F0X&pf_rd_s=center-4&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr4_i_2"
    # Use loop to fetch all the url page
    while url:
        # Updat the url
        url = fetch_imdb(url,"Adventure_IMDB")
    return



'''
This function aims to fetch all the fantasy movies and related information.
'''
def fantasy_imdb():
    # Set the initial url to fetch
    url = "https://www.imdb.com/search/title/?genres=fantasy&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=fd0c0dd4-de47-4168-baa8-239e02fd9ee7&pf_rd_r=HS270KKF3EKA0HHP3F0X&pf_rd_s=center-4&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr4_i_3"
    # Use loop to fetch all the url page
    while url:
        # Updat the url
        url = fetch_imdb(url,"Fantasy_IMDB")
    return



'''
This function aims to fetch all the comedy & romance movies and related information.
'''
def comedy_romance_imdb():
    # Set the initial url to fetch
    url = "https://www.imdb.com/search/title/?genres=comedy,romance&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=a581b14c-5a82-4e29-9cf8-54f909ced9e1&pf_rd_r=HS270KKF3EKA0HHP3F0X&pf_rd_s=center-5&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr5_i_1"
    # Use loop to fetch all the url page
    while url:
        # Updat the url
        url = fetch_imdb(url,"Comedy_Romance_IMDB")
    return



'''
This function aims to fetch all the action & comedy movies and related information.
'''
def action_comedy_imdb():
    # Set the initial url to fetch
    url = "https://www.imdb.com/search/title/?genres=action,comedy&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=a581b14c-5a82-4e29-9cf8-54f909ced9e1&pf_rd_r=HS270KKF3EKA0HHP3F0X&pf_rd_s=center-5&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr5_i_2"
    # Use loop to fetch all the url page
    while url:
        # Updat the url
        url = fetch_imdb(url,"Action_Comedy_IMDB")
    return



'''
This function aims to fetch all the superhero movies and related information.
'''
def superhero_imdb():
    # Set the initial url to fetch
    url = "https://www.imdb.com/search/keyword/?keywords=superhero&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=a581b14c-5a82-4e29-9cf8-54f909ced9e1&pf_rd_r=HS270KKF3EKA0HHP3F0X&pf_rd_s=center-5&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr5_i_3"
    # Use loop to fetch all the url page
    while url:
        # Updat the url
        url = fetch_superhero_imdb(url,"Superhero_IMDB")
    return



