from bs4 import BeautifulSoup
import requests
import random
from datetime import datetime
import time
from dotenv import load_dotenv
import os
import tweepy
import calendar
from pycoingecko import CoinGeckoAPI
import schedule


def main():
    variables_initialization()
    while True:
        for i in range(5):
            stakings_list[i].update(get_txn(urls[i], stakings_list[i], staking_time[i]))
        schedule.run_pending()
        print("Wait 2 min")
        time.sleep(120)


def job(daily):
    try:
        sfund_price = coin_api.get_price(ids='seedify-fund', vs_currencies='usd')
    except:
        time.sleep(2)
        sfund_price = coin_api.get_price(ids='seedify-fund', vs_currencies='usd')

    sfund_worth_in = round(float(daily['in']) * sfund_price['seedify-fund']['usd'], 2)
    sfund_worth_out = round(float(daily['out']) * sfund_price['seedify-fund']['usd'], 2)
    client.create_tweet(text=(
        f'$SFUND depostied and withdrawn from all pools in past 24h:\n\n\n➡  DEPOSITED: {round(daily["in"],2):,} SFUND worth {sfund_worth_in:,}$\n\n⬅  WITHDRAWN: {round(daily["out"],2):,} SFUND worth {sfund_worth_out:,}$'))
    print("POSTED SUMMARY")
    daily_post_reset()



def post(data, staking_time):
    global daily
    if data["IO"] == "IN":
        daily["in"] += data["amount"]
    else:
        daily["out"] += data["amount"]

    print(data)

    if data["amount"] >= 5000:
        # check SFUND price by using coingeco API
        emotes = ""
        try:
            sfund_price = coin_api.get_price(ids='seedify-fund', vs_currencies='usd')
        except:
            time.sleep(2)
            sfund_price = coin_api.get_price(ids='seedify-fund', vs_currencies='usd')

        sfund_worth = round(float(data['amount']) * sfund_price['seedify-fund']['usd'], 2)
        if data["IO"] == "IN":
            if data["amount"] < 10000:
                emotes += "🔥"
            elif data["amount"] < 20000:
                emotes += "🔥🔥🔥"
            else:
                emotes += "🔥🔥🔥🔥🔥"

            client.create_tweet(text=(
                f"{emotes}  {data['amount']:,} SFUND worth {sfund_worth:,}$ was staked for {staking_time} days. More details here: https://bscscan.com/tx/{data['txn']}"))
            print("POSTED")
        else:
            if data["amount"] < 10000:
                emotes += "⚠️"
            elif data["amount"] < 20000:
                emotes += "⚠️⚠️⚠️"
            else:
                emotes += "⚠️⚠️⚠️⚠️⚠️"
            client.create_tweet(text=(
                f"{emotes}  {data['amount']:,} SFUND worth {sfund_worth:,}$ was unstaked from {staking_time} days pool. More details here: https://bscscan.com/tx/{data['txn']}"))
            print("POSTED")


def get_txn(contract, staking, staking_time):
    while True:
        header = get_agents()
        html = requests.get(f"https://bscxplorer.com/address/{contract}?filter=1", headers=header, timeout=5)
        if html.status_code == 200:
            break
    html = html.text

    soup = BeautifulSoup(html, 'lxml')
    tablerows = soup.find("ul", class_="block-list mt-6").find_all("li",
                                                                   class_="is-highlighted has-text-centered-touch is-success")
    first_txn = {}
    for row in tablerows:
        hash = row.find("a", class_="is-size-6 mempool-hash mb-0").text
        if hash == staking["txn"]:
            break
        amount = float(row.find("div", class_="level-item token-balance").find("p").text.strip("SFUND"))
        amount = round(amount, 2)

        IO = row.find("div", class_="level-item token-balance").find("p")["class"]
        if "success" in IO[2]:
            IO = "IN"
        else:
            IO = "OUT"

        date = row.find_all("div", class_="level-item")[1].text
        date = date_formating(date)
        stacting_date = datetime.strptime(staking["date"], '%d/%m/%y %H:%M:%S')

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
    return first_txn


def date_formating(date):
    date = date.split(", ")[1]
    date = date.split(" UTC")[0]
    month_to_num = dict((month, str(index)) for index, month in enumerate(calendar.month_abbr) if month)
    date = date.split(" ")
    date = date[0] + "/" + month_to_num[date[1]] + "/" + date[2][2:] + " " + date[3]
    date = datetime.strptime(date, '%d/%m/%y %H:%M:%S')
    return date

def daily_post_reset():
    global daily
    daily = {
        "in": 0,
        "out": 0
    }
    print("Reseted")

def variables_initialization():
    global staking7, staking14, staking30, staking60, staking90, stakings_list, staking_time, client, urls, coin_api, schedule

    global daily
    daily = {
        "in": 0,
        "out": 0
    }
    schedule.every().day.at("12:00").do(job, daily=daily)

    coin_api = CoinGeckoAPI()

    staking7 = {
        "txn": "",
        "amount": 0,
        "IO": "",
        "date": datetime.utcnow().strftime('%d/%m/%y %H:%M:%S')
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

    return {"user-agent": random.choice(user_agents)}



main()