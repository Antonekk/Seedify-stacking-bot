from bs4 import BeautifulSoup
import requests
import time

html = requests.get("https://bscscan.com/address/0xb667c499b88ac66899e54e27ad830d423d9fba69#tokentxns").text
soup = BeautifulSoup(html, 'lxml')
print(soup)
