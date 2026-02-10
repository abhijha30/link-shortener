from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import random, string, os, qrcode

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(os.getcwd(), "static", "qr_codes")
os.makedirs(STATIC_DIR, exist_ok=True)

DB_PATH = os.path.join(BASE_DIR, "urls.db")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + DB_PATH
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), nullable=False)
    short_code = db.Column(db.String(10), unique=True, nullable=False)
    clicks = db.Column(db.Integer, default=0)
    qr_code = db.Column(db.String(200))

def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        long_url = request.form.get("url")
        short_code = generate_short_code()

        short_url = request.host_url + short_code

        # Generate QR Code
        qr_img = qrcode.make(short_url)
        qr_filename = f"{short_code}.png"
        qr_path = os.path.join(STATIC_DIR, qr_filename)
        qr_img.save(qr_path)

        new_url = URL(
            original_url=long_url,
            short_code=short_code,
            qr_code=f"/static/qr_codes/{qr_filename}"
        )

        db.session.add(new_url)
        db.session.commit()

        return render_template(
            "result.html",
            short_url=short_url,
            qr_code=new_url.qr_code
        )

    return render_template("index.html")

@app.route("/<short_code>")
def redirect_url(short_code):
    url = URL.query.filter_by(short_code=short_code).first_or_404()
    url.clicks += 1
    db.session.commit()
    return redirect(url.original_url)

with app.app_context():
    db.create_all()
