import requests
from bs4 import BeautifulSoup
import smtplib
import time

# The URL of the product you want to track prices for
URL = 'https://www.amazon.de/adidas-Herren-Powerlift-Multisport-Indoor/dp/B07RGLT5P9?pf_rd_p=0f6687bc-b0cb-44d9-9696-138c1879ad4f&pd_rd_wg=dYnko&pf_rd_r=T2JN66ZVCRNKWMJDNRAD&ref_=pd_gw_cr_simh&pd_rd_w=OZtBM&pd_rd_r=6840f8e9-226d-4d03-bfd8-69f6215493e6'

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"}

def check_price():

    page = requests.get(URL, headers=headers)
    
    soup = BeautifulSoup(page.content, 'html.parser')
    
    title = soup.find(id="productTitle").get_text()
    price = soup.find(id="priceblock_ourprice").get_text()
    
    # The price converted from string to float - only checks the first 2 characters of the string
    converted_price = float(price[0:2])
    
    # The price you are looking for
    if(converted_price < 59):
        send_mail()
    
    print(converted_price)
    print(title.strip())
    
def send_mail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    
    # I use two step verification and generated password through Google's App Passwords
    # It's the email that you send from
    server.login('your_mail', 'your_password')
    
    subject = 'Price fell down!'
    body = 'Check the amazon link: https://www.amazon.de/adidas-Herren-Powerlift-Multisport-Indoor/dp/B07RGLT5P9?pf_rd_p=0f6687bc-b0cb-44d9-9696-138c1879ad4f&pd_rd_wg=dYnko&pf_rd_r=T2JN66ZVCRNKWMJDNRAD&ref_=pd_gw_cr_simh&pd_rd_w=OZtBM&pd_rd_r=6840f8e9-226d-4d03-bfd8-69f6215493e6'
    
    msg = f"Subject: {subject}\n\n{body}"
    
    # You can send it to any number of email accounts
    server.sendmail(
            'your_mail',
            'your_mail',
            msg
            )
    print('Hey, email has been sent')
    server.quit()
    
# It checks the price in every hour
while(True):
    check_price()
    time.sleep(3600)