############################### RUNS THE SITE ###############################

# NOTE: KEEP THIS SCRIPT CLEAN AND BASICALLY IMPORT ALL METHODS FROM OTHER PYTHON FILES WE WRITE

############# IMPORTS#############
# LIBRARIES
from flask import Flask, render_template, request, redirect, url_for, flash, session, g
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
# from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import SelectField
from datetime import datetime
from bs4 import BeautifulSoup
import functools
import requests
import os

# FILES
import db_connect as db

import landing
import login
import signup

import profile_recom as pr
import profile_edit as prof_edit
import profile_history as prof_hist
import poster_image as pi
import service_recc as sr
import imdb_database as imdb_db

############# START UP CONFIGURATION #############
# app configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'
# Configuring variables for user file uploads
app.config['UPLOAD_FOLDER'] = 'recc_syst'
ALLOWED_EXTENSIONS = {'xls','xlsx','csv','png','jpg','jpeg','gif'}


############# CLASSES AND METHODS #############
'''
Class for form object: Specifically drop-down menus for individual recommendations

Inherits from FlaskForm

Created by Jessica 04.27
'''
class ReccDropForm(FlaskForm):
    rent = SelectField('rent_title', choices=[([],"Select a movie or tv show")], default="Select a movie or tv show")
    buy = SelectField('buy_title', choices=[([],"Select a movie or tv show")], default="Select a movie or tv show")

'''
Check if user id is stored in session

Created by Jessica - 04.27
'''
@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = db.get_db().execute('''SELECT * FROM all_user_data WHERE userID="{user_id}"'''.format(user_id=user_id)).fetchone()

'''
Decorator to check if user is logged into a session 
Determines access to certain pages and visible header buttons (in browsing sections)

Input:
Returns:

Created by Jessica - 04.27
'''
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('login'))
        return view(**kwargs)
    return wrapped_view

'''
Verifies that user uploaded file has a valid extension 

Input: filename
Returns:

Created by Jessica - 05.01
'''
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS


############# PAGES #############

############################### LANDING SEGMENT ###############################
# landing page
@app.route('/')
def home():
    page = landing.bootstrap_landing()
    return page
# above is format for all methods below:
    # actual render_template all done in main methods of individual py scripts
    # that is returned up to this central file

################# SIGN UP #################
# sign up page
@app.route('/signup', methods=('GET', 'POST'))
def sign_up():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        fname = request.form['first'].strip()
        lname = request.form['last'].strip()
        email = request.form['email'].strip()
        join_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conn = db.get_db()
        error = None

        # grabbing all possible errors
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not fname:
            error = 'First name is required.'
        elif not lname:
            error = 'Last name is required.'
        elif not email:
            error = 'Email is required.'
        elif conn.execute('''SELECT EXISTS(SELECT * FROM all_user_data WHERE username="{username}")'''.format(username=username)).fetchone()[0] == 1:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            conn.execute('''INSERT INTO all_user_data (userID, username, password, fname, lname, email, join_date, user_bio, linked_amazon, linked_netflix, linked_hbo, linked_hulu) VALUES (default, "{username}", "{password}", "{fname}", "{lname}", "{email}", "{join_date}","", FALSE, FALSE, FALSE, FALSE)'''.format(username=username,password=password,fname=fname,lname=lname,email=email,join_date=join_date))
            return redirect(url_for('login'))

        flash(error)

    return render_template('bootstrap-login-signup.html')

# # sign up succeed page
# @app.route('/signup/success')
# def sign_up_success():
#     # page = signup.success() # METHOD DOES NOT EXIST?
#     page = "Successful sign up"
#     return page

# # import watchlist - sign up version
# @app.route('/signup/watchimport')
# def sign_up_watchImport():
#     page = "Sign Up through Importing list"
#     return page

################# LOG IN AND OUT #################
# log in page
@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password1 = request.form['password']
        conn = db.get_db()
        error = None
        user = conn.execute('''SELECT * FROM all_user_data WHERE username="{username}"'''.format(username=username)).fetchone()

        # grabbing all possible errors
        if not username:
            error = 'Username is required.'
        elif not password1:
            error = 'Password is required.'
        elif user is None:
            error = 'Incorrect username.'
        elif user['password'] != password1:
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['userID']
            return redirect(url_for('profile_edit', username=username))

        flash(error)

    return render_template('bootstrap-login-login.html')

# log out page
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


############################### BROWSING SEGMENT ###############################
# movie/show search page
@app.route('/browse', methods=('GET', 'POST'))
def browse():
    # genre image galleries
    galleries = {'comedy':{'page':'Comedy', 'cards':[]}, 'sci-fi':{'page':'Sci-Fi', 'cards':[]}, 'horror': {'page':'Horror', 'cards':[]}, 'romance': {'page':'Romance', 'cards':[]}, 'action': {'page':'Action', 'cards':[]}, 'thriller': {'page':'Thriller', 'cards':[]}, 'drama': {'page':'Drama', 'cards':[]}, 'mystery': {'page':'Mystery', 'cards':[]}, 'crime': {'page':'Crime', 'cards':[]}, 'animation': {'page':'Animation', 'cards':[]}, 'adventure': {'page':'Adventure', 'cards':[]}, 'fantasy':{'page':'Fantasy', 'cards':[]}}

    for gen in galleries.keys():
        galleries[gen]['cards'] = imdb_db.top_six_imdb(gen)
    # print(galleries)

    # search bar hit submit
    if request.method == "POST":
        # Connect to database
        conn = db.get_db()

        # Query for search from table "IMDb_Catalog"
        exact_query = conn.execute('''SELECT title, year, imdbID FROM IMDb_Catalog WHERE title = "{search_title}"'''.format(search_title=request.form['search'])).fetchall()
        imdb_query = conn.execute('''SELECT title, year, imdbID FROM IMDb_Catalog WHERE title LIKE "%%{search_title}%%"'''.format(search_title=request.form['search'])).fetchall()

        # results to list
        results = []
        # already have
        already_id = set()

        for cont in exact_query:
            cleanYear = cont['year']
            if cleanYear[1] == 'I': cleanYear = cleanYear[4:]

            cleanPoster = pi.get_poster_url(cont['imdbID'])

            results.append({'title': cont['title'],'imdbID': cont['imdbID'],'year':cleanYear,'image_url': cleanPoster})
            already_id.add(cont['imdbID'])

        for cont in imdb_query:
            if cont['imdbID'] not in already_id:
                cleanYear = cont['year']
                if cleanYear[1] == 'I': 
                    cleanYear = cleanYear[cleanYear[4:].find("(")+4:]

                cleanPoster = pi.get_poster_url(cont['imdbID'])

                results.append({'title': cont['title'],'imdbID': cont['imdbID'],'year':cleanYear,'image_url': cleanPoster})

        conn.close()
        return render_template('browse-search.html', results=results, galleries=galleries)

        # return render_template("results.html", records=c.fetchall())
    return render_template('browse-search.html', galleries=galleries)

# movie/show content page: the contents of this method should honestly be sent to a separate file
@app.route('/browse/<imdbID>')
def browse_content(imdbID):
    # connect to database
    conn = db.get_db()
    # query for piece of content's row from the table "IMDb_Catalog"
    imdb_query = conn.execute('''SELECT * FROM IMDb_Catalog WHERE imdbID = "{imdbID}"'''.format(imdbID=imdbID)).fetchone()
    if imdb_query == None:
        return render_template('browse-content-missing.html')

    # query for content in table "Parsed_Catalog"
    parsed_query = conn.execute('''SELECT * FROM Parsed_Catalog WHERE imdbID = "{imdbID}"'''.format(imdbID=imdbID)).fetchone()

    # items to pack
    title = imdb_query['title']

    year = imdb_query['year']
    if year[1] == 'I':
        year = year[year[4:].find("(")+4:]

    genres = imdb_query['genres'].split(", ")
    imdb_rating = imdb_query['IMDb_rating']

    certificates = imdb_query['certificate']
    if certificates == None or certificates == "Unrated" or certificates == "Not Rated":
        certificates = ""

    description = imdb_query['intro']
    if description.find("Add a Plot") != -1:
        description = ""
    if description.find("See full summary") != -1:
        # shortcut for now
        description = ""
        # need to retrieve and update table with correct summary. 
        # plot_page = BeautifulSoup(requests.get("https://www.imdb.com/title/{imdbID}/plotsummary".format(imdbID=imdbID)).text, 'html.parser')
    
    poster = pi.get_poster_url(imdbID)

    director = imdb_query['director']
    if director == None:
        director = ""
    else:
        director = director.split(", ")

    stars = imdb_query['star']
    if stars == None:
        stars = ""
    else:
        stars = stars.split(", ")

    platforms = []
    individuals = dict()

    # check if content wasn't in "Parsed_Catalog"
    if parsed_query == None:
        # adding to Parsed_Catalog table
        utelly_call = sr.call_Utelly(imdbID, imdb_query['title'])

        if utelly_call == False:
            return render_template('browse-content-missing.html')

        if utelly_call['subscription']['amazon prime'] == True:
            platforms.append("Amazon Prime Video")
        if utelly_call['subscription']['netflix'] == True:
            platforms.append("Netflix")
        if utelly_call['subscription']['hbo'] == True:
            platforms.append('HBO')
        if utelly_call['subscription']['hulu'] == True:
            platforms.append('Hulu')

        individuals = utelly_call['individual']

        nowhere = False
        # check nowhere
        if utelly_call['individual']['google'][1] == 0.0 and utelly_call['individual']['itunes'][1] == 0.0 and utelly_call['subscription']['amazon prime'] == False and utelly_call['subscription']['netflix'] == False and utelly_call['subscription']['hbo'] == False and utelly_call['subscription']['hulu'] == False:
            nowhere = True

        # insert into database
        conn.execute('''INSERT INTO Parsed_Catalog (imdbID, title, google_rent, google_buy, google_url, itunes_rent, itunes_buy, itunes_url, amazon_prime, netflix, hbo, hulu, nowhere) VALUES ("{imdbID}","{title},{google_rent}, {google_buy}, "{google_url}", {itunes_rent}, {itunes_buy}, "{itunes_url}", {amazon_prime}, {netflix}, {hbo}, {hulu}, {nowhere})'''.format(imdbID=imdbid,title=title,google_rent=utelly_call['individual']['google'][0],google_buy=utelly_call['individual']['google'][1],itunes_rent=utelly_call['individual']['itunes'][0],itunes_buy=utelly_call['individual']['itunes'][1],amazon_prime=utelly_call['subscription']['amazon prime'],netflix=utelly_call['subscription']['netflix'],hbo=utelly_call['subscription']['hbo'],hulu=utelly_call['subscription']['hulu'],nowhere=nowhere))
    else:
        if parsed_query['amazon_prime'] == True:
            platforms.append("Amazon Prime Video")
        if parsed_query['netflix'] == True:
            platforms.append("Netflix")
        if parsed_query['hbo'] == True:
            platforms.append('HBO')
        if parsed_query['hulu'] == True:
            platforms.append('Hulu')

        individuals['google'] = (parsed_query['google_rent'],parsed_query['google_buy'])
        individuals['itunes'] = (parsed_query['itunes_rent'],parsed_query['itunes_buy'])
        

    # packaged information for sending off to template
    page = {"title":title,
            "year":year, # check for that weird (I) (year) thing
            "genres":genres, # break into list so can click towards browse by genre pages
            "IMDb_rating":imdb_rating,
            "certificates":certificates, # if certificates are null or not rated, don't show
            "description":description, # need to check if scrape was cut off and update table with full
            "poster_url":poster,
            "platforms":platforms,
            "individuals":individuals,
            "director":director,
            "stars":stars}

    conn.close()
    return render_template('browse-content.html', page=page)

############################### PROFILE SEGMENT ###############################

################# EDIT #################
# user profile main page; auto routes to edit profile page
@app.route('/<username>/profile')
@app.route('/<username>/profile/edit')
@login_required
def profile_edit(username):
    # get user bio
    bio = prof_edit.get_bio(username)

    # get user top three genre
    top_three = prof_edit.three_genre(prof_edit.ranked_genre(username))
    
    # get information for author card
    card = prof_edit.get_card(username)

    # need to be able to edit author cards later
    profile = {'username':username,
                'fname': card['fname'],
                'lname': card['lname'],
                'join_month': card['join_month'],
                'join_year': card['join_year'],
                'bio': bio,
                'top_three':top_three}

    return render_template('profile/profile-edit.html', profile=profile, username=username)

@app.route('/<username>/profile/edit-bio', methods=('GET', 'POST'))
@login_required
def profile_edit_bio(username):
    # get info for author card
    card = prof_edit.get_card(username)

    # get user existing bio
    bio = prof_edit.get_bio(username)

    # pack info for author card and page
    profile = {'username':username,
                'fname': card['fname'],
                'lname': card['lname'],
                'join_month': card['join_month'],
                'join_year': card['join_year'],
                'bio': bio}

    if request.method == 'POST':
        bio_body = request.form['bio_body']
        prof_edit.update_sql_bio(username, bio_body)
        return redirect(url_for('profile_edit', username=username))

    return render_template('profile/profile-edit-bio.html', profile=profile, username=username)

################# HISTORY #################
# user profile history and watchlist page
@app.route('/<username>/profile/history')
@login_required
def profile_history(username):
    # get info for author card
    card = prof_edit.get_card(username)

    # list of watchlist tables and files
    watchlists = []

    # connect to database to get existing watchlist names
    conn = db.get_db()
    user_lists = conn.execute('''SELECT DISTINCT watchlist_name FROM IMDb_Watchlist WHERE username="{username}"'''.format(username=username)).fetchall()
    for ent in user_lists:
        # get preview of watchlist
        preview_query = conn.execute('''SELECT Const, Title FROM IMDb_Watchlist WHERE username="{username}" AND watchlist_name="{watchlist_name}" LIMIT 4'''.format(username=username, watchlist_name=ent['watchlist_name'])).fetchall()
        preview_list = []
        for row in preview_query:
            preview_list.append({'imdbid':row['Const'], 'title':row['Title'], 'url':pi.get_poster_url_sql(row['Const'],row['Title'])})
        print(preview_list)
        # put name of list and preview into list
        watchlists.append({"name":ent['watchlist_name'],"preview":preview_list})

    # list of recent videos; restrict to 4 titles - FROM BROWSING, CONVERT FROM HARDCODE
    recents = []
    # TESTING HARDCODE DUMMY
    recents.extend([{'imdbid':'tt0105236','title':'Reservoir Dogs','url':''},
                    {'imdbid':'tt4975722','title':'Moonlight','url':''},
                    {'imdbid':'tt0475784','title':'Westworld','url':''},
                    {'imdbid':'tt3322314','title':'Luke Cage','url':''}])
    for rec in recents:
        rec['url'] = pi.get_poster_url_sql(rec['imdbid'],rec['title'])

    # dictionary containing page content
    page = {'watchlists': watchlists,
            'recents': recents }
    return render_template('profile/profile-history.html', profile=card, page=page, username=username)

# page from user profile specifically to a watchlist
@app.route('/<username>/profile/watchlist/<watch_name>', methods=('GET', 'POST'))
@login_required
def profile_watchlist_each(username, watch_name):
    # get info for author card
    card = prof_edit.get_card(username)
    
    # watchlist name
    watchlist = prof_hist.parse_watchlist_for_page(username,watch_name)

    return render_template('/profile/profile-watchlist-each.html', profile=card, watch_name=watch_name, watchlist=watchlist, username=username)

# # trying to get pagination on watchlist pages
# # COME BACK TO THIS LATER

# # loading pagination
# @app.route('/profile/watchlist/<watch_name>/<int:page>', methods=['GET'])
# def view(page = 1):
#     per_page = 1
#     max_per_page = 20
#     # content = paginate(page, per_page, error_out=True, max_per_page)
#     # posts = Posts.query.order_by(Posts.time.desc()).paginate(page,per_page,error_out=False)
#     return render_template('/profile/profile-pagination.html', posts=posts)

# user adding watchlist
@app.route('/<username>/profile/watchlist/add', methods=('GET','POST'))
@login_required
def profile_watchlist_add(username):
    # get info for author card
    card = prof_edit.get_card(username)

    # User submits action; Uploading a file overrides constructing watchlist through browsing
    if request.method == 'POST':
        # Get name of watchlist
        # check that don't already have this title for a watchlist
        watchlist_title = request.form['title']

        # Get description of watchlist

        # User uploads watchlist
        # checks if post request has file part
        if 'file' in request.files:
            uploaded = request.files['file']
            if uploaded and allowed_file(uploaded.filename):
                filename = secure_filename(uploaded.filename)
                uploaded.save(os.path.join(app.config['UPLOAD_FOLDER'], username+"_"+filename))
                # NOTE: optimally, want to figure out a way to parse without having to actually save the file

                # parse through file
                db.create_watchlist_upload(username, watchlist_title,os.path.join(app.config['UPLOAD_FOLDER'], username+"_"+filename))

                return redirect(url_for('profile_watchlist_add',username=username,filename=filename))

    return render_template('/profile/profile-watchlist-add.html', profile=card, username=username)

# guide for how to import IMDb watchlist
@app.route('/tutorial/upload-imdb')
def tutorial_upload_imdb():
    return render_template('tutorial-upload-imdb.html')

################# RECOMMENDATION #################
# streaming service recommendation
@app.route('/<username>/profile/recommendation', methods=['GET','POST'])
@login_required
def profile_recommendation(username):
    # get info for author card
    card = prof_edit.get_card(username)

    # gets main content loaded onto screen
    page_content = pr.main(username)
    drops = ReccDropForm()
    drops.rent.choices.extend([([ind_cont['platform'],ind_cont['price']],ind_cont['title']) for ind_cont in page_content['indiv_rents']])
    drops.buy.choices.extend([([ind_cont['platform'],ind_cont['price']],ind_cont['title']) for ind_cont in page_content['indiv_buys']])

    return render_template('profile/profile-recommendation.html', profile=card, service_recc=page_content['service_recc'], indiv_rents=page_content['indiv_rents'], indiv_buys=page_content['indiv_buys'], plat_content=page_content['plat_content'], drop_form=drops, username=username)

################# SECURITY #################
# user profile security and login page
@app.route('/<username>/profile/security', methods=('GET', 'POST'))
@login_required
def profile_security(username):
    # get info for author card
    card = prof_edit.get_card(username)

    # connect to db
    conn = db.get_db()
    
    # dictionary for items to put into input boxes of page
    form_input = conn.execute('''SELECT username, password, email FROM all_user_data WHERE username="{username}"'''.format(username=username)).fetchone()
    form_dic = {'username':form_input['username'],'password':form_input['password'],'email':form_input['email']}

    # update database from submitting change to form
    if request.method == 'POST':
        # OH WHOOPS NEED TO ADDRESS DUPLICATES WHEN CHANGING USERNAME
        # update_username = conn.execute('''UPDATE all_user_data SET username="{username}" WHERE ''')
        update_password = conn.execute('''UPDATE all_user_data SET password="{password}" WHERE username="{username}"'''.format(password=request.form['password'], username=username))
        update_email = conn.execute('''UPDATE all_user_data SET email="{email}" WHERE username="{username}"'''.format(email=request.form['email'],username=username))

        return redirect(url_for('profile_security', username=username))

    conn.close()

    return render_template('profile/profile-security.html', profile=card, username=username, form_dic=form_dic)

################# LINKED #################
# user profile linked accounts page
@app.route('/<username>/profile/linked')
@login_required
def profile_linked(username):
    # get info for author card
    card = prof_edit.get_card(username)
    
    # get boolean statuses from sql
    linked = db.linked_account_status(username)

    return render_template('profile/profile-linked.html', profile=card, linked=linked, username=username)

# updating which linked accounts user has
@app.route('/<username>/profile/linked/update', methods=('GET', 'POST'))
@login_required
def profile_linked_update(username):
    # get info for author card
    card = prof_edit.get_card(username)
    
    # get boolean statuses from sql
    linked = db.linked_account_status(username)

    # get form response to store updated info into database
    if request.method == 'POST':
        # posting information to database
        if request.form.get('amazon_prime') is not None:
            db.update_account_status(username,'linked_amazon',True)
        if request.form.get('netflix') is not None:
            db.update_account_status(username,'linked_netflix',True)
        if request.form.get('hbo') is not None:
            db.update_account_status(username,'linked_hbo',True)
        if request.form.get('hulu') is not None:
            db.update_account_status(username,'linked_hulu',True)

        return redirect(url_for('profile_linked', username=username))

    return render_template('profile/profile-linked-update.html', profile=card, linked=linked, username=username)

################# PREFERENCES #################
# user profile content preferences page
@app.route('/<username>/profile/preferences')
@login_required
def profile_preferences(username):
    # get info for author card
    card = prof_edit.get_card(username)
    
    # page = "Profile preferences page"
    return render_template('profile/profile-preference.html', profile=card, username=username)

################# INCOMPLETE #################
# # import watchlist - user profile version
# # INCOMPLETE TEMPLATE
# # SEE WATCHLIST ADD INSTEAD
# @app.route('/profile/import')
# @login_required
# def profile_import():
# #    page = "Profile import page"
#     return render_template('profile/profile-generic.html')

# watchlist pages
# INCOMPLETE TEMPLATE
@app.route('/watchlist')
@login_required
def profile_watchlist():
    # will have arguments in url for each unique watchlist
#    page = "Profile watchlist page"
    return render_template('profile/profile-generic.html')

# refining user preference page
# INCOMPLETE TEMPLATE
@app.route('/recommendation/refine')
@login_required
def profile_recommendation_refine():
    page = "Profile recommentation refine page"
    return page

# results page


############################### FOOTER SEGMENT ###############################
# about us page
@app.route('/about')
def about():
    # return render_template('one-column-footer-page.html', title="About Us", page_content=page_content)
    return render_template('footer/footer-about.html')

# contact us page
@app.route('/contact')
def contact():
    # return render_template('one-column-footer-page.html', title="Contact Us", page_content=page_content)
    return render_template('footer/footer-contact.html')

# privacy policy page
@app.route('/privacy')
def privacy():
    # return render_template('one-column-footer-page.html', title="Privacy Policy", page_content=page_content)
    return render_template('footer/footer-privacy.html')

# FAQ page
@app.route('/faq')
def faq():
    # return render_template('one-column-footer-page.html', title="FAQ", page_content=page_content)
    return render_template('footer/footer-faq.html')

# # Requires different template from above
# # sitemap page
# @app.route('/sitemap')
# def sitemap():
#     page = "Sitemap page"
#     return page

# Report bugs page
@app.route('/bugs', methods=('GET','POST'))
def bugs():
    if request.method == 'POST':
        # bio_body = request.form['bio_body']
        # prof_edit.update_sql_bio(username, bio_body)
        conn = db.get_db()
        conn.execute('''INSERT INTO reported_bugs (logNum, report_name, report_content) VALUES (default, "{name}","{content}")'''.format(name=request.form['name'],content=request.form['report']))
        return redirect(url_for('bugs_success'))

    return render_template('footer/footer-report.html')

# successfully submitted bug report
@app.route('/bugs/success')
def bugs_success():
    return render_template('footer/footer-report-success.html')


############################### OLD TESTS SEGMENT ###############################
# # TESTING FOOTER
# @app.route('/test')
# def test_page():
#     return render_template('header-footer.html')

# @app.route('/test/bootstrap')
# def test_bootstrap():
#     return render_template('bootstrap_template.html')

# @app.route('/test/justwatch')
# def test_justwatch():
#     return render_template('test-justwatch.html')

# @app.route('/test/profile-gen-kitty')
# def test_profile_gen_kitty():
#     return render_template('profile/profile-generic.html')


###############################
app.run(host='0.0.0.0', port=5000, debug=True)
# app.run(host='35.245.57.180', port=5000, debug=True)