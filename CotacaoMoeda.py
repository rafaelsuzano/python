from urllib.request import urlopen
import re
import sys
import datetime
import time

import pyodbc

server = 'rafaelsuzano.database.windows.net'
database = 'rafaelsuzano'
username = 'rafaelsuzano'
password = 'suz@no30'
driver= '{ODBC Driver 13 for SQL Server}'


print('###Consultando Moedas###') 
print ('Data da Consulta' + time.strftime(" %Y-%m-%d %H:%M:%S"))

dt= (time.strftime(" %Y-%m-%d %H:%M:%S"))
cnxn = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

DEFAULT_REGEX = r'<input type="text" id="nacional" value="([^"]+)"/>'
CURRENCY = {
    'dolar': 'http://dolarhoje.com/',
    'euro': 'http://eurohoje.com/',
    'libra': 'http://librahoje.com/',
    'peso': 'http://pesohoje.com/'
}


def exchange_rate(url):
    response = urlopen(url).read().decode('utf-8')
    result = re.search(DEFAULT_REGEX, response)
    if result:
        return result.group(1)

cursor.execute ("delete from cotacao where data <= ?", (dt))

cnxn.commit()

for currency, url in CURRENCY.items():

		print('Incluindo cotação...' + currency.upper() + ' R$ '+ exchange_rate(url) )
		

		cursor.execute("insert into COTACAO (moeda,valor,fonte,data) values (?,?,?,?)",currency,exchange_rate(url),url,dt)
		cnxn.commit()

cnxn.close()
