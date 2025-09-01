import os
import smtplib
import requests
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- Gmail credentials from environment variables ---
GMAIL_USER = os.environ.get("GMAIL_USER")
GMAIL_PASS = os.environ.get("GMAIL_PASS")
TO_EMAIL = GMAIL_USER

def fetch_prices():
    url = "https://www.gasbuddy.com/station/130688"  # Costco Warden
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0.0.0 Safari/537.36"
        )
    }
    response = requests.get(url, headers=headers, timeout=15)
    if response.status_code != 200:
        print(f"Failed to fetch page. Status code: {response.status_code}")
        return "Price not available", "Price not available"

    soup = BeautifulSoup(response.text, "html.parser")

    try:
        regular_price_elem = soup.select_one(
            "div.station-price__regular span.fuel-price__price"
        )
        premium_price_elem = soup.select_one(
            "div.station-price__premium span.fuel-price__price"
        )

        regular_price = regular_price_elem.text.strip() if regular_price_elem else "Price not available"
        premium_price = premium_price_elem.text.strip() if premium_price_elem else "Price not available"

        return regular_price, premium_price
    except Exception as e:
        print(f"Error parsing HTML: {e}")
        return "Price not available", "Price not available"

def send_email(regular, premium):
    subject = "Costco Warden Gas Prices"
    body = f"Costco Warden Regular: {regular}\nCostco Warden Premium: {premium}"

    msg = MIMEMultipart()
    msg["From"] = GMAIL_USER
    msg["To"] = TO_EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_PASS)
        server.sendmail(GMAIL_USER, TO_EMAIL, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

def main():
    regular, premium = fetch_prices()
    print(f"Regular: {regular}, Premium: {premium}")
    send_email(regular, premium)

if __name__ == "__main__":
    main()
