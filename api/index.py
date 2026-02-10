from flask import Flask, render_template_string, request, redirect
import random, string, qrcode, io, base64

app = Flask(__name__)

HTML_INDEX = """
<!DOCTYPE html>
<html>
<head>
    <title>Link Shortener</title>
</head>
<body style="font-family:Arial; text-align:center; margin-top:50px;">
    <h2>🔗 Link Shortener + QR</h2>
    <form method="POST">
        <input type="url" name="url" required placeholder="Enter long URL" style="padding:10px;width:300px;">
        <br><br>
        <button type="submit" style="padding:10px 20px;">Generate</button>
    </form>
</body>
</html>
"""

HTML_RESULT = """
<!DOCTYPE html>
<html>
<head>
    <title>Result</title>
</head>
<body style="font-family:Arial; text-align:center; margin-top:50px;">
    <h3>Short URL</h3>
    <p><a href="{short_url}">{short_url}</a></p>
    <h3>QR Code</h3>
    <img src="data:image/png;base64,{qr}">
    <br><br>
    <a href="/">Create another</a>
</body>
</html>
"""

def gen_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        long_url = request.form["url"]
        code = gen_code()
        short_url = request.host_url + code

        img = qrcode.make(short_url)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        qr_base64 = base64.b64encode(buf.getvalue()).decode()

        return render_template_string(
            HTML_RESULT,
            short_url=short_url,
            qr=qr_base64
        )

    return render_template_string(HTML_INDEX)

@app.route("/<code>")
def redirect_link(code):
    return redirect("https://google.com")
