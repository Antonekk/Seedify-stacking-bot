import unicodedata
from bs4 import BeautifulSoup
import requests
import random
from datetime import datetime
import time
from dotenv import load_dotenv
import os
import tweepy



def main():
    while True:
        for i in range(5):
            stakings_list[i].update(get_txn(urls[i], stakings_list[i], staking_time[i]))
        print("wait")
        time.sleep(120)



staking7 = {
    "txn": "",
    "amount": 0,
    "IO": "",
    "date": datetime.utcnow().strftime('%y/%m/%d %H:%M:%S')
}
staking14 = dict(staking7)
staking30 = dict(staking7)
staking60 = dict(staking7)
staking90 = dict(staking7)

stakings_list = [staking7, staking14, staking30, staking60, staking90]
staking_time = ["7", "14", "30", "60", "90"]

load_dotenv()
API_KEY = os.getenv("API_KEY")
API_SECRET_KEY = os.getenv("API_SECRET_KEY")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET_TOKEN = os.getenv("ACCESS_SECRET_TOKEN")
client = tweepy.Client(consumer_key=API_KEY,
                       consumer_secret=API_SECRET_KEY,
                       access_token=ACCESS_TOKEN,
                       access_token_secret=ACCESS_SECRET_TOKEN,
                       wait_on_rate_limit=True)

urls = ["0xb667c499b88ac66899e54e27ad830d423d9fba69",
        "0x027fC3A49383D0E7Bd6b81ef6C7512aFD7d22a9e",
        "0x8900475BF7ed42eFcAcf9AE8CfC24Aa96098f776",
        "0x66b8c1f8DE0574e68366E8c4e47d0C8883A6Ad0b",
        "0x5745b7E077a76bE7Ba37208ff71d843347441576"]


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

    return {"user-agent": random.choice(user_agents), "cookie": "ASP.NET_SessionId=n1af0r3hfibrwtsf3kmk1phe; __stripe_mid=a774203e-9120-4797-b6d0-d41b29fa29f1eaa03e; bscscan_cookieconsent=True; bscscan_userid=Antonek; bscscan_pwd=4792:Qdxb:n2uINnhrZ+dCxSvLK7BvdPAhyITjuvSg3abwwgSwZjc=; bscscan_autologin=True; __cuid=eb8642842bb0485889e91524ed494a9c; amp_fef1e8=2c12ba0d-95ab-4614-a8ad-d53ac353fae8R...1gc6dfp1b.1gc6dfp1f.t.3.10; __cflb=02DiuJNoxEYARvg2sN5n1HeVcoKCZ1njFYGe1E8j1jB7r; __cf_bm=dbdh4.hBaIA7tGn4PC_rB1OeU.pqWo3KD9gJGWi9Cf8-1662893333-0-ARzLn+/SAG3n/18GxJvCUh1TtNu3XLDU0L2QrsCpgq+i+RDZN+zAFVk2zPIEAsli169k2D1FMmq82SJsNI6nsLb8SKMMXWi82/92+Ym4awRlhg42E9Rm3f/uxs75RLCwhw=="}



def post(data, staking_time):
    if data["amount"] > 250:
        if data["IO"] == "IN":
            client.create_tweet(text=(f"{data['amount']} SFUND was staked for {staking_time} days. More details here: https://bscscan.com/tx/{data['txn']}"))
            print("POSTED")
        else:
            client.create_tweet(text=(f"{data['amount']} SFUND was unstaked from {staking_time} days pool. More details here: https://bscscan.com/tx/{data['txn']}"))
            print("POSTED")


def get_txn(contract, staking, staking_time):
    while True:
        header = get_agents()
        html = requests.get(f"https://bscscan.com/tokentxns?a={contract}", headers=header, timeout=5, proxies={"http": "https://167.99.41.64:3128"})
        print(html.status_code)
        if html.status_code == 200:
            break
    html = html.text

    soup = BeautifulSoup(html, 'lxml')
    tablerows = soup.find("table", class_="table table-text-normal table-hover").tbody.find_all("tr")
    first_txn = {}
    for row in tablerows:
        token = row.find("img").parent.text
        if "SFUND" not in token:
            break
        hash = row.find("a",class_="myFnExpandBox_searchVal").text
        if hash == staking["txn"]:
            break
        amount = round(float( (row.find_all("td")[7].text).replace(",", "") ),2)
        IO = unicodedata.normalize("NFKD",row.find_all("td")[5].text).strip()

        date = row.find_all("td")[3].span["title"].replace("-", "/")
        date = date[2:4] + date[4:]
        date = datetime.strptime(date, '%y/%m/%d %H:%M:%S')
        stacting_date = datetime.strptime(staking["date"], '%y/%m/%d %H:%M:%S')

        if date > stacting_date:
            transaction = {
                "txn": hash,
                "amount": amount,
                "IO": IO,
                "date": date.strftime('%y/%m/%d %H:%M:%S')
            }
            post(transaction, staking_time)
            if not first_txn:
                first_txn = transaction
        else:
            break
    return  first_txn

main()
