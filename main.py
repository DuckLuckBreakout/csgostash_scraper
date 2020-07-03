import time
from csgostash import CsgoStashScraper
from tele_bot import TeleBot


if __name__ == '__main__':
    last_hour = -1
    while True:
        hour_now = int(time.strftime('%H', time.localtime(time.time())))
        if hour_now != last_hour:
            TeleBot().send_new_file_info(str(str(time.ctime())))
            with open(str(time.ctime()), 'w') as output:
                output.write(str(CsgoStashScraper().full_data))
                last_hour = int(time.strftime('%H', time.localtime(time.time())))


