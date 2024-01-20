from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)
current_year = datetime.now().year


@app.route('/')
def homepage():
    return render_template('index.html', year=current_year)


@app.route('/description')
def post_page():
    return render_template('single.html')


if __name__ == '__main__':
    app.run(debug=True)
