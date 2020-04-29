##############################################
# This file aims to do web scraping for differnt genres on IMDb website.

# Created by Kitty - 4.29
##############################################
from bs4 import BeautifulSoup
import requests
##############################################
#            GLOBAL VARIABLES

COMEDY_URL = "https://www.imdb.com/search/title/?genres=comedy&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=3396781f-d87f-4fac-8694-c56ce6f490fe&pf_rd_r=HS270KKF3EKA0HHP3F0X&pf_rd_s=center-1&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr1_i_1"

SCIFI_URL = "https://www.imdb.com/search/title/?genres=sci-fi&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=3396781f-d87f-4fac-8694-c56ce6f490fe&pf_rd_r=HS270KKF3EKA0HHP3F0X&pf_rd_s=center-1&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr1_i_2"

HORROR_URL = "https://www.imdb.com/search/title/?genres=horror&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=3396781f-d87f-4fac-8694-c56ce6f490fe&pf_rd_r=HS270KKF3EKA0HHP3F0X&pf_rd_s=center-1&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr1_i_3"

ROMANCE_URL = "https://www.imdb.com/search/title/?genres=romance&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=e0da8c98-35e8-4ebd-8e86-e7d39c92730c&pf_rd_r=HS270KKF3EKA0HHP3F0X&pf_rd_s=center-2&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr2_i_1"

ACTION_URL = "https://www.imdb.com/search/title/?genres=action&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=e0da8c98-35e8-4ebd-8e86-e7d39c92730c&pf_rd_r=HS270KKF3EKA0HHP3F0X&pf_rd_s=center-2&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr2_i_2"

THRILLER_URL = "https://www.imdb.com/search/title/?genres=thriller&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=e0da8c98-35e8-4ebd-8e86-e7d39c92730c&pf_rd_r=HS270KKF3EKA0HHP3F0X&pf_rd_s=center-2&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr2_i_3"

DRAMA_URL = "https://www.imdb.com/search/title/?genres=drama&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=f1cf7b98-03fb-4a83-95f3-d833fdba0471&pf_rd_r=HS270KKF3EKA0HHP3F0X&pf_rd_s=center-3&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr3_i_1"

MYSTERY_URL = "https://www.imdb.com/search/title/?genres=mystery&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=f1cf7b98-03fb-4a83-95f3-d833fdba0471&pf_rd_r=HS270KKF3EKA0HHP3F0X&pf_rd_s=center-3&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr3_i_2"

CRIME_URL = "https://www.imdb.com/search/title/?genres=crime&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=f1cf7b98-03fb-4a83-95f3-d833fdba0471&pf_rd_r=HS270KKF3EKA0HHP3F0X&pf_rd_s=center-3&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr3_i_3"

ANIMATION_URL = "https://www.imdb.com/search/title/?genres=animation&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=fd0c0dd4-de47-4168-baa8-239e02fd9ee7&pf_rd_r=HS270KKF3EKA0HHP3F0X&pf_rd_s=center-4&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr4_i_1"

ADVENTURE_URL = "https://www.imdb.com/search/title/?genres=adventure&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=fd0c0dd4-de47-4168-baa8-239e02fd9ee7&pf_rd_r=HS270KKF3EKA0HHP3F0X&pf_rd_s=center-4&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr4_i_2"

FANTASY_URL = "https://www.imdb.com/search/title/?genres=fantasy&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=fd0c0dd4-de47-4168-baa8-239e02fd9ee7&pf_rd_r=HS270KKF3EKA0HHP3F0X&pf_rd_s=center-4&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr4_i_3"

COMEDY_ROMANCE_URL = "https://www.imdb.com/search/title/?genres=comedy,romance&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=a581b14c-5a82-4e29-9cf8-54f909ced9e1&pf_rd_r=HS270KKF3EKA0HHP3F0X&pf_rd_s=center-5&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr5_i_1"

ACTION_COMEDY_URL = "https://www.imdb.com/search/title/?genres=action,comedy&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=a581b14c-5a82-4e29-9cf8-54f909ced9e1&pf_rd_r=HS270KKF3EKA0HHP3F0X&pf_rd_s=center-5&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr5_i_2"

SUPERHERO_URL = "https://www.imdb.com/search/keyword/?keywords=superhero&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=a581b14c-5a82-4e29-9cf8-54f909ced9e1&pf_rd_r=HS270KKF3EKA0HHP3F0X&pf_rd_s=center-5&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr5_i_3"
# STILL WORKING ON SUPERHERO URL, DIFFIRENT LAYOUT ON WEBSITE

##############################################
'''
This function requires a url as parameter (listed above), and returns a dictionary of movie information:
    title,
    poster,
    time,
    certificate,
    runtime,
    genre,
    rate,
    intro,
    director,
    star
'''
def fetch_movie(url):
    
    # Get the web page
    page = requests.get(url)
    bs = BeautifulSoup(page.text, 'html.parser')
    
    # Create dictionary to store the information
    movie_dict = {}
    
    # Fetch the information
    movie_list = bs.findAll('div','lister-item mode-advanced')
    
    for movie in movie_list:
        poster = movie.find('img')['loadlate'].strip() # movie poster        
        title = movie.findAll('a')[1].text.strip() # movie title        
        time = movie.find('span','lister-item-year text-muted unbold').text.strip().strip() # movie time (published)        
        try:
            certificate = movie.find('span','certificate').text.strip() # movie certificate (R, PG-13,etc.)
        except:
            certificate = None        
        try:
            runtime = movie.find('span','runtime').text.strip() # movie runtime (hours and minutes)
        except:
            runtime = None        
        genre = movie.find('span','genre').text.strip().split(', ') # movie genre        
        try:
            rate = movie.find('div','inline-block ratings-imdb-rating').text.strip() # movie rate (out of 10)
        except:
            rate = None        
        intro = movie.findAll('p','text-muted')[1].text.strip() # movie introduction/description        
        para = movie.findAll('p')[2].text.strip().replace(', ','').split('\n')        
        if '| ' in para:
            director = para[1:para.index('| ')] # movie director 
            star = para[para.index('| ')+2:] # movie star (if contains movie director)
        else:
            director = None
            star = para[1:] # movie star (if not contains movie director)
        
        # Store the information
        movie_dict[title] = {'poster':poster,
                              'time':time,
                              'certificate':certificate,
                              'runtime':runtime,
                              'genre':genre,
                              'rate':rate,
                              'intro':intro,
                              'director':director,
                              'star':star
                             }
           
    return movie_dict

