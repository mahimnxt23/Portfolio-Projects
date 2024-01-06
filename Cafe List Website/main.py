from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)
current_year = datetime.now().year


@app.route('/')
def homepage():
    return render_template('index.html', year=current_year)


if __name__ == '__main__':
    app.run(debug=True)
