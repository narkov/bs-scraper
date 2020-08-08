import requests
from bs4 import BeautifulSoup
import csv

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

page_num = 0
while True:
  try:
    page_num += 1
    url = "https://atdw.com.au/our-listings/"
    json_data = {"pge": str(page_num)}
    req = requests.post(url, json=json_data)
    soup = BeautifulSoup(req.content, 'html.parser')
    divs = soup.find_all('a', {'class': 'blogbutton'})

    for div in divs:
      page = requests.get(div['href'], headers)
      soup_page  = BeautifulSoup(page.content, 'html.parser')
      head = soup_page.find('div', {'class': 'headtext'})
      title = head.h1.getText()
      address = head.p.getText().split(",")
      address1 = address[0].strip()
      address2 = address[1].strip()
      category = soup_page.find('div', {'id': 'category'}).getText()

      print (title + "," + address1 + "," + address2 + "," + category)
    
  except Exception as ex:
    print(ex)
