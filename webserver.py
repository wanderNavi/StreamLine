############################### RUNS THE SITE ###############################

# NOTE: KEEP THIS SCRIPT CLEAN AND BASICALLY IMPORT ALL METHODS FROM OTHER PYTHON FILES WE WRITE

############# IMPORTS#############
# LIBRARIES
from flask import Flask, render_template, request
from sqlalchemy import create_engine

# FILES
import landing
import login
import signup
import profile_recom as pr

############# GLOBAL VARIABLES #############
# CONNECT TO DATABASE

############# METHODS #############

############# PAGES #############
app = Flask(__name__)

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
    return render_template('LOGIN_TEMPLATE/signup.html')

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
    return render_template('LOGIN_TEMPLATE/login.html')



# movie/show search page
@app.route('/browse')
def browse():
    page = "Browse catalog page"
    return page

# movie/show profile page


# NOTE: IF CREATE PUBLIC PROFILE KIND OF THING, CHANGE BELOW "PROFILE" ALL INTO "SETTINGS"
# user profile main page
@app.route('/profile')
def profile():
    # auto route to edit profile page
    page = "Profile main page"
#     return page
    return render_template('profile-generic-UPDATED.html',page_title="Edit")

# user profile edit profile page
@app.route('/profile/edit')
def profile_edit():
    page = "Profile edit page" 
#     return page
    return render_template('profile-generic-UPDATED.html',page_title="Edit")

# user profile history and watchlist page
@app.route('/profile/history')
def profile_history():
    page = "Profile history page"
    return render_template('profile-generic-UPDATED.html',page_title="History")

# streaming service recommendation
@app.route('/profile/recommendation')
def profile_recommendation():
#     page = "Profile recommendation page"
    page = pr.main('profile-generic-UPDATED.html','Parsed_Watchlist_Sample')
    return page

# user profile security and login page
@app.route('/profile/security')
def profile_security():
#    page = "Profile security page"
    return render_template('profile-generic-UPDATED.html',page_title="Security")

# user profile linked accounts page
@app.route('/profile/linked')
def profile_linked():
#    page = "Profile linked page"
    return render_template('profile-generic-UPDATED.html',page_title="Linked")

# user profile content preferences page
@app.route('/profile/preferences')
def profile_preferences():
#    page = "Profile preferences page"
    return render_template('profile-generic-UPDATED.html',page_title="Preference")

# import watchlist - user profile version
@app.route('/profile/import')
def profile_import():
#    page = "Profile import page"
    return render_template('profile-generic-UPDATED.html')

# watchlist pages
@app.route('/watchlist')
def profile_watchlist():
    # will have arguments in url for each unique watchlist
#    page = "Profile watchlist page"
    return render_template('profile-generic-UPDATED.html')

# refining user preference page
@app.route('/recommendation/refine')
def profile_recommendation_refine():
    page = "Profile recommentation refine page"
    return page

# results page



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
    return render_template('profile-generic-UPDATED.html')

# about us page
@app.route('/about')
def about():
    page_content = ['This is the about page.', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ultricies ullamcorper ante et placerat. Integer ut diam nec ipsum condimentum aliquet ut ac leo. Sed pretium velit nisi, sed pulvinar ante porta vel. Suspendisse et posuere ex. Etiam tincidunt tempor turpis, quis lacinia tellus ultricies ac. Nam rutrum orci nulla, vitae dictum nulla vulputate a. Morbi libero sapien, sollicitudin eu nisi id, posuere porta urna. Morbi gravida elit nisl, eu gravida arcu pretium id. Vivamus magna mi, fermentum in placerat vel, tincidunt tincidunt purus.', 'Integer condimentum magna mattis nisi condimentum, sollicitudin luctus ligula elementum. Sed rhoncus ante quis sollicitudin dictum. Pellentesque finibus lectus quis nibh ullamcorper aliquam. Cras sed aliquet sapien. Vivamus blandit tempor turpis nec condimentum. Phasellus ornare id dui a tincidunt. Morbi congue mi quis tempor cursus. In ac suscipit dui, id efficitur turpis. Phasellus varius leo eget dolor pellentesque consequat. Nam eu libero nisl. Sed consectetur ante elit, in commodo diam interdum quis. Aenean feugiat porta est vitae condimentum. Cras ornare ante tellus, sed mattis ligula egestas tempus. Donec sodales tellus mi, non ultricies diam auctor et. Quisque congue venenatis mauris, non convallis felis sodales a.', 'Donec aliquet lectus vitae mi consequat, vitae rutrum orci tempus. Suspendisse at erat quis nisl elementum molestie. Proin aliquet gravida posuere. Aenean vitae lobortis ipsum. Integer blandit massa enim. Donec consectetur tellus ut lorem venenatis gravida ac eu velit. Etiam auctor mauris nulla, sit amet euismod libero eleifend at. Ut risus est, elementum vitae augue dapibus, laoreet convallis sem. Vestibulum eget erat sapien. Curabitur non placerat libero, eu feugiat nisl.']
    return render_template('one-column-footer-page.html', title="About Us", page_content=page_content)

# contact us page
@app.route('/contact')
def contact():
    page_content = ['This is the contact page.', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ultricies ullamcorper ante et placerat. Integer ut diam nec ipsum condimentum aliquet ut ac leo. Sed pretium velit nisi, sed pulvinar ante porta vel. Suspendisse et posuere ex. Etiam tincidunt tempor turpis, quis lacinia tellus ultricies ac. Nam rutrum orci nulla, vitae dictum nulla vulputate a. Morbi libero sapien, sollicitudin eu nisi id, posuere porta urna. Morbi gravida elit nisl, eu gravida arcu pretium id. Vivamus magna mi, fermentum in placerat vel, tincidunt tincidunt purus.', 'Integer condimentum magna mattis nisi condimentum, sollicitudin luctus ligula elementum. Sed rhoncus ante quis sollicitudin dictum. Pellentesque finibus lectus quis nibh ullamcorper aliquam. Cras sed aliquet sapien. Vivamus blandit tempor turpis nec condimentum. Phasellus ornare id dui a tincidunt. Morbi congue mi quis tempor cursus. In ac suscipit dui, id efficitur turpis. Phasellus varius leo eget dolor pellentesque consequat. Nam eu libero nisl. Sed consectetur ante elit, in commodo diam interdum quis. Aenean feugiat porta est vitae condimentum. Cras ornare ante tellus, sed mattis ligula egestas tempus. Donec sodales tellus mi, non ultricies diam auctor et. Quisque congue venenatis mauris, non convallis felis sodales a.', 'Donec aliquet lectus vitae mi consequat, vitae rutrum orci tempus. Suspendisse at erat quis nisl elementum molestie. Proin aliquet gravida posuere. Aenean vitae lobortis ipsum. Integer blandit massa enim. Donec consectetur tellus ut lorem venenatis gravida ac eu velit. Etiam auctor mauris nulla, sit amet euismod libero eleifend at. Ut risus est, elementum vitae augue dapibus, laoreet convallis sem. Vestibulum eget erat sapien. Curabitur non placerat libero, eu feugiat nisl.']
    return render_template('one-column-footer-page.html', title="Contact Us", page_content=page_content)

# privacy policy page
@app.route('/privacy')
def privacy():
    page_content = ['This is the privacy page.', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ultricies ullamcorper ante et placerat. Integer ut diam nec ipsum condimentum aliquet ut ac leo. Sed pretium velit nisi, sed pulvinar ante porta vel. Suspendisse et posuere ex. Etiam tincidunt tempor turpis, quis lacinia tellus ultricies ac. Nam rutrum orci nulla, vitae dictum nulla vulputate a. Morbi libero sapien, sollicitudin eu nisi id, posuere porta urna. Morbi gravida elit nisl, eu gravida arcu pretium id. Vivamus magna mi, fermentum in placerat vel, tincidunt tincidunt purus.', 'Integer condimentum magna mattis nisi condimentum, sollicitudin luctus ligula elementum. Sed rhoncus ante quis sollicitudin dictum. Pellentesque finibus lectus quis nibh ullamcorper aliquam. Cras sed aliquet sapien. Vivamus blandit tempor turpis nec condimentum. Phasellus ornare id dui a tincidunt. Morbi congue mi quis tempor cursus. In ac suscipit dui, id efficitur turpis. Phasellus varius leo eget dolor pellentesque consequat. Nam eu libero nisl. Sed consectetur ante elit, in commodo diam interdum quis. Aenean feugiat porta est vitae condimentum. Cras ornare ante tellus, sed mattis ligula egestas tempus. Donec sodales tellus mi, non ultricies diam auctor et. Quisque congue venenatis mauris, non convallis felis sodales a.', 'Donec aliquet lectus vitae mi consequat, vitae rutrum orci tempus. Suspendisse at erat quis nisl elementum molestie. Proin aliquet gravida posuere. Aenean vitae lobortis ipsum. Integer blandit massa enim. Donec consectetur tellus ut lorem venenatis gravida ac eu velit. Etiam auctor mauris nulla, sit amet euismod libero eleifend at. Ut risus est, elementum vitae augue dapibus, laoreet convallis sem. Vestibulum eget erat sapien. Curabitur non placerat libero, eu feugiat nisl.']
    return render_template('one-column-footer-page.html', title="Privacy Policy", page_content=page_content)

# FAQ page
@app.route('/faq')
def faq():
    page_content = ['This is the faq page.', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ultricies ullamcorper ante et placerat. Integer ut diam nec ipsum condimentum aliquet ut ac leo. Sed pretium velit nisi, sed pulvinar ante porta vel. Suspendisse et posuere ex. Etiam tincidunt tempor turpis, quis lacinia tellus ultricies ac. Nam rutrum orci nulla, vitae dictum nulla vulputate a. Morbi libero sapien, sollicitudin eu nisi id, posuere porta urna. Morbi gravida elit nisl, eu gravida arcu pretium id. Vivamus magna mi, fermentum in placerat vel, tincidunt tincidunt purus.', 'Integer condimentum magna mattis nisi condimentum, sollicitudin luctus ligula elementum. Sed rhoncus ante quis sollicitudin dictum. Pellentesque finibus lectus quis nibh ullamcorper aliquam. Cras sed aliquet sapien. Vivamus blandit tempor turpis nec condimentum. Phasellus ornare id dui a tincidunt. Morbi congue mi quis tempor cursus. In ac suscipit dui, id efficitur turpis. Phasellus varius leo eget dolor pellentesque consequat. Nam eu libero nisl. Sed consectetur ante elit, in commodo diam interdum quis. Aenean feugiat porta est vitae condimentum. Cras ornare ante tellus, sed mattis ligula egestas tempus. Donec sodales tellus mi, non ultricies diam auctor et. Quisque congue venenatis mauris, non convallis felis sodales a.', 'Donec aliquet lectus vitae mi consequat, vitae rutrum orci tempus. Suspendisse at erat quis nisl elementum molestie. Proin aliquet gravida posuere. Aenean vitae lobortis ipsum. Integer blandit massa enim. Donec consectetur tellus ut lorem venenatis gravida ac eu velit. Etiam auctor mauris nulla, sit amet euismod libero eleifend at. Ut risus est, elementum vitae augue dapibus, laoreet convallis sem. Vestibulum eget erat sapien. Curabitur non placerat libero, eu feugiat nisl.']
    return render_template('one-column-footer-page.html', title="FAQ", page_content=page_content)

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