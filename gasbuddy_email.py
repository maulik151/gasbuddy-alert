import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

# --- Gmail credentials from environment variables ---
GMAIL_USER = os.environ.get("GMAIL_USER")
GMAIL_PASS = os.environ.get("GMAIL_PASS")
TO_EMAIL = GMAIL_USER

def fetch_prices():
    options = Options()
    options.add_argument("--headless=new")   # headless mode for GitHub Actions
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get("https://www.gasbuddy.com/station/130688")
        wait = WebDriverWait(driver, 15)

        # Regular
        regular_elem = wait.until(EC.presence_of_element_located((
            By.XPATH, '//*[@id="root"]/div/div[3]/div/div/div[2]/div[1]/div[1]/div[1]/div[3]/div/div[2]/div[2]/div[1]/span'
        )))
        regular_price = regular_elem.text.strip()

        # Premium
        premium_elem = wait.until(EC.presence_of_element_located((
            By.XPATH, '//*[@id="root"]/div/div[3]/div/div/div[2]/div[1]/div[1]/div[1]/div[3]/div/div[2]/div[2]/div[2]/span'
        )))
        premium_price = premium_elem.text.strip()

        return regular_price, premium_price

    except TimeoutException:
        return "Price not available", "Price not available"
    finally:
        driver.quit()

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
