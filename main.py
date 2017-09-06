# 50% done

import requests
import re
from bs4 import BeautifulSoup
import time
import random
import smtplib


def printandlog(msg):
    print(msg)
    lFile.write(msg)


def emailnotification(msg):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    # Your email password here
    server.login("iiiantong@gmail.com", "")
    server.sendmail("iiiantong@gmail.com", "iiiantong@gmail.com", msg)
    server.quit()
    printandlog("Email sent: "+msg)


# A url here
url = ''
jar = requests.cookies.RequestsCookieJar()

cFile = open('cookies.txt', 'r')
lFile = open('logs.txt', 'w')
for line in cFile:
    if not line.startswith('#'):
        data = re.split(r'\t', line.strip())
        if data.__len__() >= 7:
            jar.set(data[5], data[6], domain=data[0], path=data[2])
respond = requests.get(url, cookies=jar)
printandlog("### Cookies added")
count = 0

while True:
    count += 1
    printandlog('### ' + count.__str__() + ' attempt at      ' + time.ctime().__str__())
    printandlog('### HTML retrieved from sis.nyu.edu')
    html = respond.content.decode()
    soup = BeautifulSoup(html, 'html.parser')

    try:
        firstStatus = soup.find(id="win0divDERIVED_REGFRM1_SSR_STATUS_LONG$0").find('img').attrs["alt"]
        printandlog("--- First Status: " + firstStatus)
        if not firstStatus == "Closed":
            printandlog('!!! The first class in your shopping cart is not closed!')
            emailnotification("The first class is open!")
        else:
            printandlog('### Still closed')

    except AttributeError:
        printandlog('AttributeError')
        emailnotification("AttributeError")

    rNum = random.randrange(5, 30)
    printandlog("### Sleep for " + rNum.__str__() + "s\n")
    time.sleep(rNum)

rFile = open('respond.html', 'w')
rFile.write(html)
rFile.close()
lFile.close()
