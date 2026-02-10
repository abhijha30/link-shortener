from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import random, string, os, qrcode

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)

DB_PATH = os.path.join(BASE_DIR, "urls.db")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + DB_PATH
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

QR_DIR = os.path.join(app.static_folder, "qr_codes")
os.makedirs(QR_DIR, exist_ok=True)

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), nullable=False)
    short_code = db.Column(db.String(10), unique=True, nullable=False)
    clicks = db.Column(db.Integer, default=0)
    qr_code = db.Column(db.String(200))

def generate_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        long_url = request.form["url"]
        code = generate_code()
        short_url = request.host_url + code

        qr_img = qrcode.make(short_url)
        qr_file = f"{code}.png"
        qr_img.save(os.path.join(QR_DIR, qr_file))

        new = URL(
            original_url=long_url,
            short_code=code,
            qr_code=f"/static/qr_codes/{qr_file}"
        )

        db.session.add(new)
        db.session.commit()

        return render_template(
            "result.html",
            short_url=short_url,
            qr_code=new.qr_code
        )

    return render_template("index.html")

@app.route("/<code>")
def go(code):
    url = URL.query.filter_by(short_code=code).first_or_404()
    url.clicks += 1
    db.session.commit()
    return redirect(url.original_url)

with app.app_context():
    db.create_all()
