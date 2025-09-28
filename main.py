import os
import time
import sys
import asyncio
import trafilatura
from bs4 import BeautifulSoup

from notices.bot import Notice_Bot
from configs import logger, CSV_DIR, DELIVERY_HOUR
from utils import get_today, get_hour, make_csv_file, get_email_html, send_email


async def main():
    while True:
        today = get_today()
        hour = get_hour()
        # links
        csv_file_path = f'{CSV_DIR}/{today}.csv'
        if not os.path.exists(csv_file_path) and hour >= DELIVERY_HOUR:
            notice = Notice_Bot()
            links = notice.get_latest_links()
            make_csv_file(results=links, filename=csv_file_path)
            
            email_subject = f'[보안 business notice] {today}'
            html = get_email_html(email_subject, results=links)
            send_email(html, subject=email_subject)
        await asyncio.sleep(3600)

if __name__ == '__main__':
    logger.info('start')
    asyncio.run(main())