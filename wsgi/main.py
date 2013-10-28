from flask import Flask, render_template

application = Flask(__name__)

@application.route('/')
@application.route('/<username>')
def index(username = None):
    if username is None:
        return render_template('themes/water/index.html', page_title = 'Biography just for you!')
    return render_template('themes/water/bio.html', page_title = username)

if __name__ == '__main__':
    application.run(debug=True, host="0.0.0.0", port=9999)
