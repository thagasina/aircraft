
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import datetime, re, time, itertools, smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

start_date = datetime.datetime(2020,9,13)
days_range = 2
trip_length, min_length, max_length = 7, 6, 12
price_goal = 900
cities = 'YMQ-OSL'

tart = pd.date_range(start_date, periods=days_range).to_pydatetime().tolist()
end = pd.date_range(start_date + datetime.timedelta(days=trip_length), periods=days_range).to_pydatetime().tolist()

# Get all combinations of dates
all_dates = list(itertools.product(start, end))

departing = []
returning = []
for i in range(len(all_dates)):
    if (([x[1] for x in all_dates][i] - [x[0] for x in all_dates][i]).days > min_length) & \
            (([x[1] for x in all_dates][i] - [x[0] for x in all_dates][i]).days < max_length):

        departing.append(([x[0] for x in all_dates][i]).strftime('%Y-%m-%d'))
        returning.append(([x[1] for x in all_dates][i]).strftime('%Y-%m-%d'))
    else:
        none
for i in range(len(departing)):
departing[i]=re.sub(' 00:00:00', '', departing[i])
returning[i]=re.sub(' 00:00:00', '', returning[i])

data = []

for i in range(len(departing)):

    page = 'https://www.ca.kayak.com/flights/' + cities + '/' + departing[i] + '/' + returning[i] + '?sort=bestflight_a'
    driver = webdriver.Chrome(executable_path=r'C:\Program Files\chromedriver.exe')
    driver.get(page)
    time.sleep(15)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    my_table = soup.find(class_=['price option-text'])

    try:
        data.append(my_table.get_text())
        data[i] = int(re.sub('[^0-9]', '', data[i]))

        if data[i] < price_goal:

            # Email info
            sender = 'YOUR EMAIL ADDRESS HERE'
            password = 'YOUR EMAIL PASSWORD HERE'
            port = 465
            receive = 'EMAIL THE ALERTS SHOULD BE SENT TO'

            # Email content
            msg = MIMEMultipart()
            msg['From'] = sender
            msg['To'] = receive
            msg['Subject'] = 'Great deal on tickets found'

            body = 'Go here to see the great deal:' + re.sub('https://www.', '', page)
            msg.attach(MIMEText(body, 'plain'))
            text = msg.as_string()

            # Sending email
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com', port=port, context=context) as server:
                server.login(sender, password)
                server.sendmail(sender, receive, text)
        else:
            None
    except:
        data.append('No flights found')

driver.quit()




