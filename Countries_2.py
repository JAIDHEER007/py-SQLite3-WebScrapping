#Creating a database to store Countries' ISO Codes and other information

import requests
from bs4 import BeautifulSoup as bs
import sqlite3

#making the connection and cursor
conn = sqlite3.connect('CountriesDataCODES.db')
curr = conn.cursor()

#Creating a table named CountriesCODE
curr.execute('''CREATE TABLE IF NOT EXISTS CountriesCODE(
                    Country_Name TEXT,
                    Country_Code TEXT,
                    ISO_Code TEXT,
                    Population INTEGER,
                    Area_KM2 REAL,
                    GDP_US_Dollar TEXT
                )''')

url = 'https://countrycode.org/'
req = requests.get(url)
soup = bs(req.text,'html.parser')

table = soup.find('table',{'data-sort-name':'countrycode'})
table_rows = table.find_all('tr')[1:]
remove_coma = lambda num:int((num.replace(',','')))

transaction = 1
for table_row in table_rows:
    data = table_row.find_all('td')
    # print('='*10)
    # print('Country_Name:',)
    # print('Country_Code:',)
    # print('ISO_Code:',)
    # print('Population:',)
    # print('Area_KM2:',)
    # print('GDP_US_Dollar:',)
    # print('='*10)
    
    country_data = (data[0].text,data[1].text,data[2].text,
                    remove_coma(data[3].text),remove_coma(data[4].text),data[5].text)
                    
    curr.execute('''INSERT INTO CountriesCODE VALUES (?,?,?,?,?,?)''',country_data)
    
    if transaction % 50 == 0:
        conn.commit()
        transaction = 1
    else:
        transaction += 1

if transaction != 1:
    conn.commit()
    
curr.close()
conn.close()