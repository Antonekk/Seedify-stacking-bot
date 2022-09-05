from bs4 import BeautifulSoup
import requests
import random
from datetime import datetime

stacking7 = {
    "txn": "",
    "amount": 0,
    "IO": "",
    "date": datetime.now().strftime("%y/%m/%d %H:%M:%S")
}

def main():
    print(stacking7)
    get_txn("0xb667c499b88ac66899e54e27ad830d423d9fba69", stacking7)

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
    for row in tablerows:
        hash = row.find("a",class_="myFnExpandBox_searchVal").text
        amount = round(float( (row.find_all("td")[7].text).replace(",", "") ),2)
        IO = row.find_all("td")[5].text

        date = row.find_all("td")[3].span["title"].replace("-", "/")
        replace_str = date[2:4]
        date = replace_str + date[4:]
        date = datetime.strptime(date, '%y/%m/%d %H:%M:%S')


main()


