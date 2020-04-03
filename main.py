import requests
from bs4 import BeautifulSoup
import re
import ctypes
from datetime import datetime
import time


REQUEST_URL = 'https://groceries.morrisons.com/webshop/getAddressesForDelivery.do?improvedAccess=yes&checkout=yes'
REQUEST_COOKIES = {}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
}


def parse_span(span):
    dt_pattern = '((Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday), (\w+) (\d+)(st|nd|rd|th))'
    obj = re.search(dt_pattern, span.text)
    dt = datetime(year=2020, month=time.strptime(obj.group(3)[:3], '%b').tm_mon, day=int(obj.group(4)))
    available_pattern = '(Unavailable|Available)'
    obj = re.search(available_pattern, span.text)
    available = False if obj.group(0) == 'Unavailable' else True

    return dt, available


def run() -> None:
    sess = requests.Session()
    for k, v in REQUEST_COOKIES.items():
        sess.cookies.set(k, v)
    while True:
        res = sess.get(REQUEST_URL, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        deliveries = [booking for booking in soup.find_all('span') if 'available' in booking.text]
        for delivery in deliveries:
            dt, available = parse_span(delivery)
            ctypes.windll.user32.FlashWindow(ctypes.windll.kernel32.GetConsoleWindow(), True)

            if available:
                print('Slot available at:', dt.strftime('%A, %d %m'))
                ctypes.windll.user32.FlashWindow(ctypes.windll.kernel32.GetConsoleWindow(), True)
        time.sleep(2)


def main() -> None:
    with open('cookies.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            values = line.split('\t')
            REQUEST_COOKIES.update({values[5]: values[6].strip('\n')})

    run()


if __name__ == '__main__':
    main()
