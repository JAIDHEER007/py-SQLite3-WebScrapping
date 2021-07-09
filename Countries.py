#Creating a database to store countries' GDP

import requests
from bs4 import BeautifulSoup as bs
import sqlite3

def currToNum(currency):
    return (int((currency[1:]).replace(',','')))

def populationToNum(population):
    return (int(population.replace(',','')))

#making the connection and cursor
conn = sqlite3.connect('CountriesData.db')
curr = conn.cursor()

#Creating a table named CountriesGDP
conn.execute('''CREATE TABLE IF NOT EXISTS CountriesGDP(
                    Country_Name TEXT, 
                    GDP_nominal_Dollar INTEGER, 
                    GDP_abbrev__Dollar text, 
                    GDP_growth_Percent REAL,
                    Population INTEGER,
                    GDP_per_capita_Dollar INTEGER,
                    World_GDP_share_Percent REAL
                )''')

#Gathering Information
url = 'https://www.worldometers.info/gdp/gdp-by-country/'
req = requests.get(url)
soup = bs(req.text,'html.parser')
table = soup.find('table',{'id':'example2'})
table_rows = table.find_all('tr')

transaction = 1
for table_row in table_rows:
    data = table_row.find_all('td')
    
    if(len(data)>1):
        country_data = (data[1].text,currToNum(data[2].text),(data[3].text)[1:],
                        float((data[4].text)[:-1]),populationToNum(data[5].text),
                        currToNum(data[6].text),float((data[7].text)[:-1]))
        curr.execute('''insert into CountriesGDP values (?,?,?,?,?,?,?)''',country_data)
    
    if transaction % 20 == 0:
        conn.commit()
        transaction = 1
    else:
        transaction += 1

if transaction != 1:
    conn.commit()
    
conn.close()