from flask import render_template

def bootstrap_landing():
    ret = render_template('LANDING_TEMPLATE/landing.html')
    return ret

def main():
    ret = render_template('test_track_landing.html')
    # 04.21: Jessica modify file name
    return ret