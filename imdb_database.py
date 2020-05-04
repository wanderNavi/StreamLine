##############################################
# This file aims to do web scraping for differnt genres on IMDb website.

# Created by Kitty - 4.30
##############################################
from bs4 import BeautifulSoup
import requests
import numpy as np
import db_connect as db_conn
import poster_image as pi
##############################################
#           FUNCTIONS FOR DATABASE           #

'''
04.30 - Jessica modifications: change "index" to imdbID, rewrote create table query primary key syntax
'''
def imdb_database(table_name, imdbID, title, poster, year, certificate, runtime, genres, IMDb_rating, intro, director, star):
    # Connect to database
    con = db_conn.get_db()
    
    # Create a new table
    # create_table_query = '''CREATE TABLE IF NOT EXISTS {table} (imdbID varchar(255) PRIMARY KEY,
    #                      title varchar(255), 
    #                      poster varchar(255),
    #                      year varchar(255),
    #                      certificate varchar(255),
    #                      runtime int,
    #                      genres varchar(255),
    #                      IMDb_rating real,
    #                      intro varchar(255),
    #                      director varchar(255),
    #                      star varchar(255))'''.format(table=table_name)
    # con.execute(create_table_query)
    
    # Insert head into the table
    insert_query = '''INSERT IGNORE INTO {table} (imdbID, title, poster, year, certificate, runtime, genres, IMDb_rating,
                    intro, director, star) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''.format(table=table_name)

    # Execute query
    query_parameters = (imdbID, title, poster, year, certificate, runtime, genres, IMDb_rating, intro, director, star)
    con.execute(insert_query, query_parameters)
    
    con.close()
    # end of method
    return

'''
This function requires a url as parameter (listed above), and returns the url for the next page for iterative (not include superhero)
'''
def fetch_imdb(url, table_name):
    
    # Get the web page
    page = requests.get(url)
    bs = BeautifulSoup(page.text, 'html.parser')
    
    # # Create dictionary to store the information
    # movie_dict = {}
    
    # Fetch the information for the webpage
    movie_list = bs.findAll('div','lister-item mode-advanced')
    
    # Fetch the information for each movie
    for movie in movie_list:
        # JESSICA 04.30 NOTE: original index extracted didn't make any sense, getting much more relevant imdbID instead
        imdbID = movie.find('a')['href'][7:-1]
        poster = movie.find('img')['loadlate'].strip() # movie poster        
        title = movie.findAll('a')[1].text.strip() # movie title    
        # JESSICA 04.30 NOTE: the name "year" is much more discriptive than "time", replacing all names    
        #                     also replacing all np.nan with Null because nan confuses MySQL
        try:
            year = movie.find('span','lister-item-year text-muted unbold').text.strip() # movie time (published)        
        except:
            year = None
        try:
            certificate = movie.find('span','certificate').text.strip() # movie certificate (R, PG-13,etc.)
        except:
            certificate = None       
        try:
            runtime = int(movie.find('span','runtime').text.strip()[:-4]) # movie runtime (hours and minutes)
        except:
            runtime = None      
        # JESSICA 04.30 NOTE: there can be multiple genres for a title
        try:
            genres = movie.find('span','genre').text.strip() # movie genre      
        except:
            genres = None
        # JESSICA 04.30 NOTE: renaming "rate" to "IMDb_Rating" to be more consistent with existing table names
        try:
            IMDb_rating = movie.find('div','inline-block ratings-imdb-rating').text.strip() # movie rate (out of 10)
        except:
            IMDb_rating = None       
        intro = movie.findAll('p','text-muted')[1].text.strip() # movie introduction/description        
        para = movie.findAll('p')[2].text.strip().replace(', ','').split('\n')        
        if '| ' in para:
            director_list = para[1:para.index('| ')] # movie director 
            director = ', '.join(director_list)
            star_list = para[para.index('| ')+2:] # movie star (if contains movie director)
            star = ', '.join(star_list)
        else:
            director = None
            star_list = para[1:] # movie star (if not contains movie director)
            star = ', '.join(star_list)
        
        # print(imdbID,"\n", title,"\n", poster,"\n", year,"\n", certificate,"\n", runtime,"\n", genres,"\n", IMDb_rating,"\n", intro,"\n", director,"\n", star,"\n","\n")

        # # Store the information        
        imdb_database(table_name, imdbID, title, poster, year, certificate, runtime, genres, IMDb_rating, intro, director, star)
        print(title)

    # Fetch the link for next page
    try:
        next_page = bs.find('a','lister-page-next next-page').get('href')
        next_url = "https://www.imdb.com" + next_page
    except:
        return
    return next_url


'''
This function requires a url as parameter (listed above), and returns the url for the next page for iterative looping

MODIFICATIONS: Jessica 04.30 - see above method for notes on changes made
'''
def fetch_superhero_imdb(url, table_name):
    
    # Get the web page
    page = requests.get(url)
    bs = BeautifulSoup(page.text, 'html.parser')
    
    # # Create dictionary to store the information
    # movie_dict = {}
    
    # Fetch the information for the webpage
    movie_list = bs.findAll('div','lister-item mode-detail')
    
    # Fetch the information for each movie
    for movie in movie_list:
        imdbID = movie.find('a')['href'][7:-1]
        poster = movie.find('img')['loadlate'].strip() # movie poster        
        title = movie.findAll('a')[1].text.strip() # movie title        
        try:
            year = movie.find('span','lister-item-year text-muted unbold').text.strip().strip() # movie time (published)        
        except:
            year = np.nan  
        try:
            certificate = movie.find('span','certificate').text.strip() # movie certificate (R, PG-13,etc.)
        except:
            certificate = np.nan        
        try:
            runtime = movie.find('span','runtime').text.strip() # movie runtime (hours and minutes)
        except:
            runtime = np.nan        
        try:
            genres = movie.find('span','genre').text.strip() # movie genre     
        except:
            genres = np.nan
        try:
            IMDb_rating = movie.find('div','inline-block ratings-imdb-rating').text.strip() # movie rate (out of 10)
        except:
            IMDb_rating = np.nan        
        intro = movie.findAll('p','text-muted')[1].text.strip() # movie introduction/description        
        para = movie.findAll('p')[2].text.strip().replace(', ','').split('\n')     
        if '| ' in para:
            director_list = para[1:para.index('| ')] # movie director 
            director = ', '.join(director_list)
            star_list = para[para.index('| ')+2:] # movie star (if contains movie director)
            star = ', '.join(star_list)
        else:
            director = np.nan
            star_list = para[1:] # movie star (if not contains movie director)
            star = ', '.join(star_list)
        
        # Store the information      
        imdb_database(table_name, imdbID, title, poster, year, certificate, runtime, genres, IMDb_rating, intro, director, star)
    
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
    # url = "https://www.imdb.com/search/title/?genres=comedy&explore=title_type,genres&ref_=adv_prv"

    # Use loop to fetch all the url page
    while url:
        # Update the url
        # url = fetch_imdb(url,"Comedy_IMDB")
        url = fetch_imdb(url,"IMDb_Catalog")
        print("URL:",url,"\n")
    return


        
'''
This function aims to fetch all the sci-fi movies and related information.
'''
def scifi_imdb():
    # Set the initial url to fetch
    url = "https://www.imdb.com/search/title/?genres=sci-fi&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=3396781f-d87f-4fac-8694-c56ce6f490fe&pf_rd_r=HS270KKF3EKA0HHP3F0X&pf_rd_s=center-1&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr1_i_2"
    # Use loop to fetch all the url page
    while url:
        # Update the url
        url = fetch_imdb(url,"IMDb_Catalog")
        print("URL:",url,"\n")
    return


    
'''
This function aims to fetch all the horror movies and related information.
'''
def horror_imdb():
    # Set the initial url to fetch
    url = "https://www.imdb.com/search/title/?genres=horror&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=3396781f-d87f-4fac-8694-c56ce6f490fe&pf_rd_r=HS270KKF3EKA0HHP3F0X&pf_rd_s=center-1&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr1_i_3"
    # Use loop to fetch all the url page
    while url:
        # Update the url
        url = fetch_imdb(url,"IMDb_Catalog")
        print("\nURL:",url)
    return



'''
This function aims to fetch all the romance movies and related information.
'''
def romance_imdb():
    # Set the initial url to fetch
    url = "https://www.imdb.com/search/title/?genres=romance&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=e0da8c98-35e8-4ebd-8e86-e7d39c92730c&pf_rd_r=HS270KKF3EKA0HHP3F0X&pf_rd_s=center-2&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr2_i_1"
    # Use loop to fetch all the url page
    # page_index = 1
    # url = 
    while url:
        # Update the url
        url = fetch_imdb(url,"IMDb_Catalog")
        print("\nURL:",url)
        # page_index += 1
        # if page_index == 1000: break
    return



'''
This function aims to fetch all the action movies and related information.
'''
def action_imdb():
    # Set the initial url to fetch
    # url = "https://www.imdb.com/search/title/?genres=action&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=e0da8c98-35e8-4ebd-8e86-e7d39c92730c&pf_rd_r=HS270KKF3EKA0HHP3F0X&pf_rd_s=center-2&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr2_i_2"
    url = "https://www.imdb.com/search/title/?genres=action&start=1951&explore=title_type,genres&ref_=adv_nxt"
    # Use loop to fetch all the url page
    page_index = 1
    while url:
        # Update the url
        url = fetch_imdb(url,"IMDb_Catalog")
        print("\n",page_index,"URL:",url)
        page_index += 1
        # if page_index == 40: break
    return



'''
This function aims to fetch all the thriller movies and related information.
'''
def thriller_imdb():
    # Set the initial url to fetch
    # url = "https://www.imdb.com/search/title/?genres=thriller&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=e0da8c98-35e8-4ebd-8e86-e7d39c92730c&pf_rd_r=HS270KKF3EKA0HHP3F0X&pf_rd_s=center-2&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr2_i_3"
    url = "https://www.imdb.com/search/title/?genres=thriller&start=1951&explore=title_type,genres&ref_=adv_nxt"
    # Use loop to fetch all the url page
    page_index = 1
    while url:
        # Updat the url
        url = fetch_imdb(url,"IMDb_Catalog")
        print("\nThriller:",page_index,"URL:",url)
        page_index += 1
        if page_index == 40: break
    return



'''
This function aims to fetch all the drama movies and related information.
'''
def drama_imdb():
    # Set the initial url to fetch
    # url = "https://www.imdb.com/search/title/?genres=drama&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=f1cf7b98-03fb-4a83-95f3-d833fdba0471&pf_rd_r=HS270KKF3EKA0HHP3F0X&pf_rd_s=center-3&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr3_i_1"
    url = "https://www.imdb.com/search/title/?genres=drama&start=1951&explore=title_type,genres&ref_=adv_nxt"
    # Use loop to fetch all the url page
    page_index = 1
    while url:
        # Updat the url
        url = fetch_imdb(url,"IMDb_Catalog")
        print("\nDrama:",page_index,"URL:",url)
        page_index += 1
        if page_index == 40: break
    return



'''
This function aims to fetch all the mystery movies and related information.
'''
def mystery_imdb():
    # Set the initial url to fetch
    # url = "https://www.imdb.com/search/title/?genres=mystery&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=f1cf7b98-03fb-4a83-95f3-d833fdba0471&pf_rd_r=HS270KKF3EKA0HHP3F0X&pf_rd_s=center-3&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr3_i_2"
    url = "https://www.imdb.com/search/title/?genres=mystery&start=1951&explore=title_type,genres&ref_=adv_nxt"
    # Use loop to fetch all the url page
    page_index = 1
    while url:
        # Updat the url
        url = fetch_imdb(url,"IMDb_Catalog")
        print("\nMystery",page_index,"URL:",url)
        page_index += 1
        if page_index == 40: break
    return



'''
This function aims to fetch all the crime movies and related information.
'''
def crime_imdb():
    # Set the initial url to fetch
    # url = "https://www.imdb.com/search/title/?genres=crime&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=f1cf7b98-03fb-4a83-95f3-d833fdba0471&pf_rd_r=HS270KKF3EKA0HHP3F0X&pf_rd_s=center-3&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr3_i_3"
    url = "https://www.imdb.com/search/title/?genres=crime&start=1951&explore=title_type,genres&ref_=adv_nxt"
    # Use loop to fetch all the url page
    page_index = 1
    while url:
        # Updat the url
        url = fetch_imdb(url,"IMDb_Catalog")
        print("\nCrime",page_index,"URL:",url)
        page_index += 1
        if page_index == 40: break
    return



'''
This function aims to fetch all the animation movies and related information.
'''
def animation_imdb():
    # Set the initial url to fetch
    # url = "https://www.imdb.com/search/title/?genres=animation&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=fd0c0dd4-de47-4168-baa8-239e02fd9ee7&pf_rd_r=HS270KKF3EKA0HHP3F0X&pf_rd_s=center-4&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr4_i_1"
    url = "https://www.imdb.com/search/title/?genres=animation&start=1951&explore=title_type,genres&ref_=adv_nxt"
    # Use loop to fetch all the url page
    page_index = 1
    while url:
        # Updat the url
        url = fetch_imdb(url,"IMDb_Catalog")
        print("\nAnimation",page_index,"URL:",url)
        page_index += 1
        if page_index == 40: break
    return



'''
This function aims to fetch all the adventure movies and related information.
'''
def adventure_imdb():
    # Set the initial url to fetch
    # url = "https://www.imdb.com/search/title/?genres=adventure&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=fd0c0dd4-de47-4168-baa8-239e02fd9ee7&pf_rd_r=HS270KKF3EKA0HHP3F0X&pf_rd_s=center-4&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr4_i_2"
    url = "https://www.imdb.com/search/title/?genres=adventure&start=1951&explore=title_type,genres&ref_=adv_nxt"
    # Use loop to fetch all the url page
    page_index = 1
    while url:
        # Updat the url
        url = fetch_imdb(url,"IMDb_Catalog")
        print("\nAdventure",page_index,"URL:",url)
        page_index += 1
        if page_index == 40: break
    return



'''
This function aims to fetch all the fantasy movies and related information.
'''
def fantasy_imdb():
    # Set the initial url to fetch
    # url = "https://www.imdb.com/search/title/?genres=fantasy&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=fd0c0dd4-de47-4168-baa8-239e02fd9ee7&pf_rd_r=HS270KKF3EKA0HHP3F0X&pf_rd_s=center-4&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr4_i_3"
    url = "https://www.imdb.com/search/title/?genres=fantasy&start=1951&explore=title_type,genres&ref_=adv_nxt"
    # Use loop to fetch all the url page
    page_index = 1
    while url:
        # Updat the url
        url = fetch_imdb(url,"IMDb_Catalog")
        print("\nFantasy",page_index,"URL:",url)
        page_index += 1
        if page_index == 40: break
    return



'''
This function aims to fetch all the comedy & romance movies and related information.

NOTE: JESSICA 05.01 - THIS REPEATS comedy_imdb(); BEING IGNORED
'''
def comedy_romance_imdb():
    # Set the initial url to fetch
    url = "https://www.imdb.com/search/title/?genres=comedy,romance&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=a581b14c-5a82-4e29-9cf8-54f909ced9e1&pf_rd_r=HS270KKF3EKA0HHP3F0X&pf_rd_s=center-5&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr5_i_1"
    # Use loop to fetch all the url page
    while url:
        # Updat the url
        url = fetch_imdb(url,"IMDb_Catalog")
        print("\nURL:",url)
    return



'''
This function aims to fetch all the action & comedy movies and related information.

NOTE: JESSICA 05.01 - THIS REPEATS comedy_imdb(); BEING IGNORED
'''
def action_comedy_imdb():
    # Set the initial url to fetch
    url = "https://www.imdb.com/search/title/?genres=action,comedy&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=a581b14c-5a82-4e29-9cf8-54f909ced9e1&pf_rd_r=HS270KKF3EKA0HHP3F0X&pf_rd_s=center-5&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr5_i_2"
    # Use loop to fetch all the url page
    while url:
        # Updat the url
        url = fetch_imdb(url,"IMDb_Catalog")
        print("\nURL:",url)
    return



'''
This function aims to fetch all the superhero movies and related information.
'''
def superhero_imdb():
    # Set the initial url to fetch
    url = "https://www.imdb.com/search/keyword/?keywords=superhero&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=a581b14c-5a82-4e29-9cf8-54f909ced9e1&pf_rd_r=HS270KKF3EKA0HHP3F0X&pf_rd_s=center-5&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr5_i_3"
    # Use loop to fetch all the url page
    page_index = 1
    while url:
        # Updat the url
        url = fetch_superhero_imdb(url,"IMDb_Catalog")
        print("\nSuperhero:",page_index,"URL:",url)
        page_index += 1
        if page_index == 40: break
    return


'''
Gets top 6 most popular items from IMDb to have in "browse-search.html"

Input: string genre: genre on imdb, options are as follows: "comedy", "sci-fi", "horror", "romance", "action", "thriller", "drama", "mystery", "crime", "animation", "adventure", "fantasy"
Returns: dictionary toRet: dictionary of values to put into genre gallery

Created by Jessica 05.02
05.03 - TOO SLOW, MAKING HARDCODE TABLE IN DATABASE INSTEAD
'''
def top_six_imdb(genre):
    # create url
    url = "https://www.imdb.com/search/title/?genres={genre}&explore=title_type,genres&ref_=adv_prv".format(genre=genre)

    # Get the web page
    page = requests.get(url)
    bs = BeautifulSoup(page.text, 'html.parser')

    # Fetch the information for the webpage
    movie_list = bs.findAll('div','lister-item mode-advanced')

    # list of dictionary to return
    toRet = []
    
    # Fetch the information for each movie
    for movie in movie_list:
        # JESSICA 04.30 NOTE: original index extracted didn't make any sense, getting much more relevant imdbID instead
        imdbID = movie.find('a')['href'][7:-1]       
        title = movie.findAll('a')[1].text.strip() # movie title   

        intro = movie.findAll('p','text-muted')[1].text.strip() # movie introduction/description  
        full_synop = ""
        for ent in movie.findAll('p','text-muted')[1].findChildren():
            if str(ent).find("/title/tt") != -1:
                synop_url = str(ent)[9:str(ent).find('">See')]
                synop_page = BeautifulSoup(requests.get("https://www.imdb.com"+synop_url).text, 'html.parser')
                full_synop = synop_page.findAll('li','ipl-zebra-list__item')[0].text.strip()
        if full_synop == "": 
            full_synop = intro

        para = movie.findAll('p')[2].text.strip().replace(', ','').split('\n')        
        if '| ' in para:
            director_list = para[1:para.index('| ')] # movie director 
            director = ', '.join(director_list)
            star_list = para[para.index('| ')+2:] # movie star (if contains movie director)
            star = ', '.join(star_list)
        else:
            director = None
            star_list = para[1:] # movie star (if not contains movie director)
            star = ', '.join(star_list)

        image_url = pi.get_poster_url(imdbID)
        image_url = image_url[:27]+"780"+image_url[30:]

        if movie.find('span','lister-item-index unbold text-primary').text[0] == "7":
            break
        else:
            toRet.append({'imdbID':imdbID, 'title':title, 'synop': full_synop, 'image_url': image_url, 'director':director, 'star':star})

    # print(toRet)
        
    return toRet



'''
test function to make debugging less heinous; remove when done
'''
def test_main():
    # comedy_imdb()
    # scifi_imdb()
    # horror_imdb() 
    # romance_imdb()
    # action_imdb() 
    thriller_imdb() # INCOMPLETE
    # drama_imdb() # INCOMPLETE
    # mystery_imdb() # INCOMPLETE
    # crime_imdb() # INCOMPLETE
    # animation_imdb() # INCOMPLETE
    # fantasy_imdb() # INCOMPLETE


# test_main()