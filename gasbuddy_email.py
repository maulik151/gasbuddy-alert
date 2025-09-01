import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException

# --- Your data ---
GMAIL_USER = "try.mkoladiya@gmail.com"
GMAIL_PASS = "ycvq vgxm qhhz unah"   # App Password
TO_EMAIL = GMAIL_USER

def fetch_and_email():
    print("Fetching prices...")

    options = Options()
    options.add_argument("--headless=new")  # Run headless; comment out to debug visually
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/114.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get("https://www.gasbuddy.com/station/130688")

        wait = WebDriverWait(driver, 15)

        # Regular price
        try:
            regular_price_elem = wait.until(EC.presence_of_element_located((
                By.XPATH, '//*[@id="root"]/div/div[3]/div/div/div[2]/div[1]/div[1]/div[1]/div[3]/div/div[2]/div[2]/div[1]/span'
            )))
            regular_price = regular_price_elem.text.strip()
        except TimeoutException:
            regular_price = "Price not available"

        # Premium price
        try:
            premium_price_elem = wait.until(EC.presence_of_element_located((
                By.XPATH, '//*[@id="root"]/div/div[3]/div/div/div[2]/div[1]/div[1]/div[1]/div[3]/div/div[2]/div[2]/div[2]/span'
            )))
            premium_price = premium_price_elem.text.strip()
        except TimeoutException:
            premium_price = "Price not available"

        print("Costco Warden Regular:", regular_price)
        print("Costco Warden Premium:", premium_price)

        # Prepare email
        subject = "Costco Warden Gas Prices"
        body = f"Costco Warden Regular: {regular_price}\nCostco Warden Premium: {premium_price}"

        msg = MIMEMultipart()
        msg["From"] = GMAIL_USER
        msg["To"] = TO_EMAIL
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        # Send email
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_PASS)
        server.sendmail(GMAIL_USER, TO_EMAIL, msg.as_string())
        server.quit()

        print("Email sent successfully!")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    fetch_and_email()
