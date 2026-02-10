function generateCode(length = 6) {
  const chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
  return Array.from({ length }, () => chars[Math.floor(Math.random() * chars.length)]).join("");
}

function generate() {
  const longUrl = document.getElementById("longUrl").value;
  if (!longUrl) return alert("Enter a URL");

  const code = generateCode();
  localStorage.setItem(code, longUrl);

  const shortUrl = `${window.location.origin}/#${code}`;

  const shortLink = document.getElementById("shortUrl");
  shortLink.href = shortUrl;
  shortLink.textContent = shortUrl;

  document.getElementById("output").classList.remove("hidden");

  document.getElementById("qrcode").innerHTML = "";
  new QRCode(document.getElementById("qrcode"), shortUrl);
}

function downloadQR() {
  const img = document.querySelector("#qrcode img");
  if (!img) return;

  const a = document.createElement("a");
  a.href = img.src;
  a.download = "qr-code.png";
  a.click();
}

// Redirect logic
window.onload = () => {
  if (window.location.hash) {
    const code = window.location.hash.substring(1);
    const url = localStorage.getItem(code);
    if (url) window.location.href = url;
  }
};

