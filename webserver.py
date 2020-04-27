############################### RUNS THE SITE ###############################

# NOTE: KEEP THIS SCRIPT CLEAN AND BASICALLY IMPORT ALL METHODS FROM OTHER PYTHON FILES WE WRITE

############# IMPORTS#############
# LIBRARIES
from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from flask_wtf import FlaskForm
from wtforms import SelectField

# FILES
import db_connect as db

import landing
import login
import signup

import profile_recom as pr
import profile_edit as prof_edit
import profile_history as prof_hist
import poster_image as pi

############# START UP CONFIGURATION #############
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'

############# CLASSES #############
'''
Class for form object: Specifically drop-down menus for individual recommendations

Inherits from FlaskForm

Created by Jessica 04.27
'''
class ReccDropForm(FlaskForm):
    rent = SelectField('rent_title', choices=[([],"Select a movie or tv show")], default="Select a movie or tv show")
    buy = SelectField('buy_title', choices=[([],"Select a movie or tv show")], default="Select a movie or tv show")

############# PAGES #############

# landing page
@app.route('/')
def home():
    page = landing.bootstrap_landing()
    return page
# above is format for all methods below:
    # actual render_template all done in main methods of individual py scripts
    # that is returned up to this central file


# sign up page
@app.route('/signup')
def sign_up():
    page = signup.main()
    return render_template('bootstrap-login-signup.html')

# sign up succeed page
@app.route('/signup/success')
def sign_up_success():
    page = signup.success()
    return page

# import watchlist - sign up version
@app.route('/signup/watchimport')
def sign_up_watchImport():
    page = "Sign Up through Importing list"
    return page


# log in page
@app.route('/login')
def login():
    page = "Login Page"
    return render_template('bootstrap-login-login.html')

# log out page
@app.route('/logout')
def logout():
    page = "Log out"
    return page


# movie/show search page
@app.route('/browse')
def browse():
    page = "Browse catalog page"
    return page

# movie/show profile page

##############################################################
# PROFILE SEGMENT

# NOTE: IF CREATE PUBLIC PROFILE KIND OF THING, CHANGE BELOW "PROFILE" ALL INTO "SETTINGS"
    # SET LOGIN VERIFICATION TO SEPARATE PUBLIC AND PRIVATE CODE

# # PROFILE BLUEPRINT
# import profile
# app.register_blueprint(profile.bp)

################# EDIT #################
# user profile main page; auto routes to edit profile page
@app.route('/profile')
@app.route('/profile/edit')
def profile_edit():
    # need to make this variable through login verification
    username = "PROTOTYPE_TEST"

    # get user bio
    bio = prof_edit.get_bio(username)

    # get user top three genre
    top_three = prof_edit.three_genre(prof_edit.ranked_genre(username))
    # print(top_three)

    # need to be able to edit author cards later
    profile = {'username':username,
                'bio': bio,
                'top_three':top_three}

    # page = prof_edit.main('profile/profile-edit.html', username)
    # return page
    return render_template('profile/profile-edit.html', profile=profile)

@app.route('/profile/edit-bio', methods=('GET', 'POST'))
def profile_edit_bio():
    # come back and find way to pass this variable later, maybe /profile/edit-bio/<username>
    username = "PROTOTYPE_TEST"

    bio = prof_edit.get_bio(username)

    if request.method == 'POST':
        bio_body = request.form['bio_body']
        prof_edit.update_sql_bio(username, bio_body)
        return redirect(url_for('profile_edit'))

    profile = {'username':username,
                'bio': bio}
    return render_template('profile/profile-edit-bio.html', profile=profile)

################# HISTORY #################
# user profile history and watchlist page
@app.route('/profile/history')
def profile_history():
    # list of watchlist tables and files
    watchlists = []
    # TESTING HARDCODE, GET RID OF LATER; dictionary in list
    watchlists.append({'title':'My Watchlist', 'file':'IMDb_Watchlist_Jenny'})

    # list of recent videos; restrict to 4 titles
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
    return render_template('profile/profile-history.html', page=page)

# page from user profile specifically to a watchlist
@app.route('/profile/watchlist/<watch_name>', methods=('GET', 'POST'))
def profile_watchlist_each(watch_name):
    # watchlist name
    # watchlist = {}
    # TESTING HARDCODE, TAKE CARE IN SQL AND GET RID LATER
    watchlist = prof_hist.parse_watchlist_for_page("IMDb_Watchlist_Jenny", "Parsed_Watchlist_Jenny")

    return render_template('/profile/profile-watchlist-each.html', watch_name=watch_name, watchlist=watchlist)

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
@app.route('/profile/watchlist/add', methods=('GET','POST'))
def profile_watchlist_add():
    return render_template('/profile/profile-watchlist-add.html')

################# RECOMMENDATION #################
# streaming service recommendation
@app.route('/profile/recommendation', methods=['GET','POST'])
def profile_recommendation():
#     page = "Profile recommendation page"
    # page = pr.main('profile/profile-recommendation.html','Parsed_Watchlist_Jenny')
    # return page

    # gets main content loaded onto screen
    page_content = pr.main('Parsed_Watchlist_Jenny')
    drops = ReccDropForm()
    drops.rent.choices.extend([([ind_cont['platform'],ind_cont['price']],ind_cont['title']) for ind_cont in page_content['indiv_rents']])
    drops.buy.choices.extend([([ind_cont['platform'],ind_cont['price']],ind_cont['title']) for ind_cont in page_content['indiv_buys']])

    # # individual rent forms
    # if request.method == 'POST':
    #     return

    return render_template('profile/profile-recommendation.html', service_recc=page_content['service_recc'], indiv_rents=page_content['indiv_rents'], indiv_buys=page_content['indiv_buys'], plat_content=page_content['plat_content'], drop_form=drops)

################# SECURITY #################
# user profile security and login page
@app.route('/profile/security')
def profile_security():
#    page = "Profile security page"
    return render_template('profile/profile-security.html')

################# LINKED #################
# user profile linked accounts page
@app.route('/profile/linked')
def profile_linked():
    # get boolean statuses from sql
    # eventually route directly to account page

    # TESTING HARDCODE WHILE MYSQL IS DOING SOMETHING WEIRD
    linked = {'amazon_prime':True, 'netflix': True, 'hbo': True, 'hulu': True}

#    page = "Profile linked page"
    return render_template('profile/profile-linked.html', linked=linked)

# updating which linked accounts user has
@app.route('/profile/linked/update')
def profile_linked_update():
    # get form response to store updated info into database
    
    # TESTING HARDCODE WHILE MYSQL IS DOING SOMETHING WEIRD
    linked = {'amazon_prime':True, 'netflix': True, 'hbo': True, 'hulu': True}

    return render_template('profile/profile-linked-update.html', linked=linked)

################# PREFERENCES #################
# user profile content preferences page
@app.route('/profile/preferences')
def profile_preferences():
#    page = "Profile preferences page"
    return render_template('profile/profile-preference.html')

# import watchlist - user profile version
# INCOMPLETE TEMPLATE
@app.route('/profile/import')
def profile_import():
#    page = "Profile import page"
    return render_template('profile/profile-generic.html')

# watchlist pages
# INCOMPLETE TEMPLATE
@app.route('/watchlist')
def profile_watchlist():
    # will have arguments in url for each unique watchlist
#    page = "Profile watchlist page"
    return render_template('profile/profile-generic.html')

# refining user preference page
# INCOMPLETE TEMPLATE
@app.route('/recommendation/refine')
def profile_recommendation_refine():
    page = "Profile recommentation refine page"
    return page

# results page


##############################################################
# OPTIONAL TEST PAGES
# TESTING FOOTER
@app.route('/test')
def test_page():
    return render_template('header-footer.html')

@app.route('/test/bootstrap')
def test_bootstrap():
    return render_template('bootstrap_template.html')

@app.route('/test/justwatch')
def test_justwatch():
    return render_template('test-justwatch.html')

@app.route('/test/profile-gen-kitty')
def test_profile_gen_kitty():
    return render_template('profile/profile-generic.html')

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

# Requires different template from above
# sitemap page
@app.route('/sitemap')
def sitemap():
    page = "Sitemap page"
    return page

# Requires different template form above
# Report bugs page
@app.route('/bugs')
def bugs():
    page = "Report bugs page"
    return page


###############################
app.run(host='0.0.0.0', port=5000, debug=True)
# app.run(host='35.245.57.180', port=5000, debug=True)