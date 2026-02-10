from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import string, random, os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500))
    short_code = db.Column(db.String(10), unique=True)
    clicks = db.Column(db.Integer, default=0)

def generate_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        long_url = request.form['url']
        code = generate_code()

        new_url = URL(original_url=long_url, short_code=code)
        db.session.add(new_url)
        db.session.commit()

        short_url = request.host_url + code
        return render_template('result.html', short_url=short_url)

    return render_template('index.html')

@app.route('/<code>')
def redirect_url(code):
    url = URL.query.filter_by(short_code=code).first_or_404()
    url.clicks += 1
    db.session.commit()
    return redirect(url.original_url)

with app.app_context():
    db.create_all()
