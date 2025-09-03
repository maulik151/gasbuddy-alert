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


def fetch_prices(station_name, url, regular_xpath, premium_xpath):
    """Fetch regular and premium prices from a GasBuddy station page."""
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/114.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    prices = {}

    try:
        driver.get(url)
        wait = WebDriverWait(driver, 15)

        # Regular price
        try:
            regular_price_elem = wait.until(EC.presence_of_element_located((By.XPATH, regular_xpath)))
            prices["regular"] = regular_price_elem.text.strip()
        except TimeoutException:
            prices["regular"] = "Price not available"

        # Premium price
        try:
            premium_price_elem = wait.until(EC.presence_of_element_located((By.XPATH, premium_xpath)))
            prices["premium"] = premium_price_elem.text.strip()
        except TimeoutException:
            prices["premium"] = "Price not available"

    finally:
        driver.quit()

    return station_name, prices


def send_email(results):
    """Send email with fetched prices."""
    subject = "Gas Prices Update"
    body_lines = []
    for station, prices in results:
        body_lines.append(f"{station} Regular: {prices['regular']}")
        body_lines.append(f"{station} Premium: {prices['premium']}")
        body_lines.append("")  # blank line between stations
    body = "\n".join(body_lines)

    msg = MIMEMultipart()
    msg["From"] = GMAIL_USER
    msg["To"] = TO_EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(GMAIL_USER, GMAIL_PASS)
    server.sendmail(GMAIL_USER, TO_EMAIL, msg.as_string())
    server.quit()


if __name__ == "__main__":
    stations = [
        ("Costco Warden", "https://www.gasbuddy.com/station/130688",
         '//*[@id="root"]/div/div[3]/div/div/div[2]/div[1]/div[1]/div[1]/div[3]/div/div[2]/div[2]/div[1]/span',
         '//*[@id="root"]/div/div[3]/div/div/div[2]/div[1]/div[1]/div[1]/div[3]/div/div[2]/div[2]/div[2]/span'),

        ("Costco Etobicoke", "https://www.gasbuddy.com/station/11791",
         '//*[@id="root"]/div/div[3]/div/div/div[2]/div[1]/div[1]/div[1]/div[3]/div/div[2]/div[2]/div[1]/span',
         '//*[@id="root"]/div/div[3]/div/div/div[2]/div[1]/div[1]/div[1]/div[3]/div/div[2]/div[2]/div[3]/span')
    ]

    results = []
    for station in stations:
        results.append(fetch_prices(*station))

    send_email(results)
    print("Email sent successfully!")
