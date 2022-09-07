import unicodedata

from bs4 import BeautifulSoup
import requests
import random
from datetime import datetime
import time

stacking7 = {
    "txn": "",
    "amount": 0,
    "IO": "",
    "date": datetime.now().strftime('%y/%m/%d %H:%M:%S')
}
stacking14 = stacking30 = stacking60 = stacking90 = stacking7

urls = {
    "7days" : "0xb667c499b88ac66899e54e27ad830d423d9fba69",
    "14days" : "0x027fC3A49383D0E7Bd6b81ef6C7512aFD7d22a9e",
    "30days" : "0x8900475BF7ed42eFcAcf9AE8CfC24Aa96098f776",
    "60days" : "0x66b8c1f8DE0574e68366E8c4e47d0C8883A6Ad0b",
    "90days" : "0x5745b7E077a76bE7Ba37208ff71d843347441576"
}

def main():
    print(stacking7)
    stacking7.update(get_txn(urls["7days"], stacking7))
    print(stacking7)

def post(data):
    print("Post was added")

def get_agents():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
        "Mozilla/5.0 (X11; Linux i686; rv:97.0) Gecko/20100101 Firefox/97.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 12.2; rv:97.0) Gecko/20100101 Firefox/97.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_2_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 OPR/83.0.4254.27",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 OPR/83.0.4254.27",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 OPR/83.0.4254.27"
    ]

    return {"user-agent": random.choice(user_agents)}

def get_txn(contract, stacking):
    header = get_agents()
    html = requests.get(f"https://bscscan.com/tokentxns?a={contract}", headers=header, timeout=5).text

    soup = BeautifulSoup(html, 'lxml')
    tablerows = soup.find("table", class_="table table-text-normal table-hover").tbody.find_all("tr")
    first_txn = {}
    for row in tablerows:
        hash = row.find("a",class_="myFnExpandBox_searchVal").text
        if hash == stacking["txn"]:
            break
        amount = round(float( (row.find_all("td")[7].text).replace(",", "") ),2)
        IO = unicodedata.normalize("NFKD",row.find_all("td")[5].text).strip()

        date = row.find_all("td")[3].span["title"].replace("-", "/")
        date = date[2:4] + date[4:]
        date = datetime.strptime(date, '%y/%m/%d %H:%M:%S')
        stacting_date = datetime.strptime('22/09/07 5:20:30', '%y/%m/%d %H:%M:%S')

        if date > stacting_date:
            transaction = {
                "txn": hash,
                "amount": amount,
                "IO": IO,
                "date": date
            }
            post(transaction)
            if not first_txn:
                first_txn = transaction
        else:
            break
    return  first_txn

main()


