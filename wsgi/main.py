from flask import Flask, render_template

application = Flask(__name__)

@application.route('/<username>')
def index(username):
    print username
    return render_template('water/index.html')

if __name__ == '__main__':
    application.run(debug=True, host="0.0.0.0", port=9999)
