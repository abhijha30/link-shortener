from flask import Flask, render_template, request, redirect
import random, string, os, qrcode

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)

def generate_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        long_url = request.form["url"]
        code = generate_code()
        short_url = request.host_url + code

        qr_dir = os.path.join(app.static_folder, "qr_codes")
        os.makedirs(qr_dir, exist_ok=True)

        qr_img = qrcode.make(short_url)
        qr_img.save(os.path.join(qr_dir, f"{code}.png"))

        return render_template(
            "result.html",
            short_url=short_url,
            qr_code=f"/static/qr_codes/{code}.png"
        )

    return render_template("index.html")

@app.route("/<code>")
def redirect_link(code):
    return redirect("https://google.com")  # TEMP redirect to test routing
