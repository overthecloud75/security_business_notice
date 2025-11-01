import os
import asyncio

from notices import Notice_Bot, get_nara_bid_info, get_latest_links_from_db
from configs import logger, CSV_DIR, DELIVERY_HOUR
from utils import get_today, get_hour, make_csv_file, get_email_html, send_email


async def main():
    while True:
        today = get_today()
        hour = get_hour()
        # links
        csv_file_path = f'{CSV_DIR}/{today}.csv'
        try:
            if not os.path.exists(csv_file_path) and hour >= DELIVERY_HOUR:
                notice = Notice_Bot()
                get_nara_bid_info()
                links = get_latest_links_from_db()
                make_csv_file(results=links, filename=csv_file_path)
                
                email_subject = f'[보안 입찰/교육/행사] {today} 주요 정보 요약'
                html = get_email_html(email_subject, results=links)
                send_email(html, subject=email_subject)
        except Exception as e:
            logger.error(e, exc_info=True)
        await asyncio.sleep(3600)

if __name__ == '__main__':
    logger.info('start')
    asyncio.run(main())