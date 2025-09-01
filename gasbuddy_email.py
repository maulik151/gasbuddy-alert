import smtplib
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

# 🔴 Replace these with your Gmail + App Password (not your normal password)
GMAIL_USER = "try.mkoladiya@gmail.com"
GMAIL_PASS = "ikux tuhi lawv xtab"

def fetch_gas_price():
    url = "https://www.gasbuddy.com/station/130688"  # Costco Warden station URL

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    time.sleep(5)

    try:
        regular = driver.find_element(By.XPATH, "//div[contains(text(),'Regular')]/following-sibling::div").text
    except:
        regular = "Price not available"

    try:
        premium = driver.find_element(By.XPATH, "//div[contains(text(),'Premium')]/following-sibling::div").text
    except:
        premium = "Price not available"

    driver.quit()
    return regular, premium

def send_email(subject, body):
    recipient = GMAIL_USER  # send to yourself

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = GMAIL_USER
    msg["To"] = recipient

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_PASS)
            server.sendmail(GMAIL_USER, recipient, msg.as_string())
        print("✅ Email sent successfully")
    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == "__main__":
    regular, premium = fetch_gas_price()
    body = f"Regular: {regular}, Premium: {premium}"
    print("Fetched Prices →", body)
    send_email("GasBuddy Price Update", body)
