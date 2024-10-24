import bs4
import urllib.request
import smtplib
import time
import imaplib

prices_list = []
lowest_price={}
def check_price():
    url1= 'https://www.amazon.in/gp/product/B01N4EV2TL/ref=ewc_pr_img_2?smid=AJ6SIZC8YQDZX&th=1'

    sauce = urllib.request.urlopen(url1).read()
    soup = bs4.BeautifulSoup(sauce, "html.parser")

    prices = soup.find(id="corePriceDisplay_desktop_feature_div").get_text()
    prices = float(prices.replace(",", "").replace("₹", ""))
    prices_list.append(prices)
    return prices

def sendemail():
	
'''def send_email(message, 'tonyalaxzendre542@gmail.com',pword, 'piyushbhatt2480@gmail.com'):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login('tonyalaxzendre542@gmail.com', pword)
    s.sendmail('tonyalaxzendre542@gmail.com', 'piyushbhatt2480@gmail.com', message)
    s.quit()'''

def price_decrease_check(price_list):
    if prices_list[-1] < prices_list[-2]:
        return True
    else:
        return False

count = 1
while True:
    current_price = check_price()
    if count > 1:
        flag = price_decrease_check(prices_list)
        if flag:
            decrease = prices_list[-1] - prices_list[-2]
            message = f"The price has decrease please check the item. The price decrease by {decrease} rupees."
#            send_email(message) #ADD THE OTHER AGRUMENTS 'tonyalaxzendre542@gmail.com', pword, 'piyushbhatt2480@gmail.com'
            lowest_price["lowest till now is"]=prices_list[-1]
    time.sleep(24600)
    count += 1
pword="lorem ipsum"
print(lowest_price)
