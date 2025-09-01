import os
import smtplib
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

def fetch_gas_price():
    url = "https://www.gasbuddy.com/station/130688"  # Costco Warden station URL

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")  # headless for GitHub Actions
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    time.sleep(5)  # wait for JS to load

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
    user = os.getenv("GMAIL_USER")
    pwd = os.getenv("GMAIL_PASS")
    recipient = os.getenv("GMAIL_USER")  # send to yourself

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = user
    msg["To"] = recipient

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(user, pwd)
            server.sendmail(user, recipient, msg.as_string())
        print("✅ Email sent successfully")
    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == "__main__":
    regular, premium = fetch_gas_price()
    body = f"Regular: {regular}, Premium: {premium}"
    send_email("GasBuddy Price Update", body)
