import os
import time

from notices import Notice_Bot, get_nara_bid_info, get_links_from_db
from configs import logger, CSV_DIR, DELIVERY_HOUR
from utils import get_today, get_hour, make_csv_file, html_template, send_email


def business_notice():
    today = get_today()
    hour = get_hour()
    # links
    csv_file_path = f'{CSV_DIR}/{today}.csv'
    try:
        if not os.path.exists(csv_file_path) and hour >= DELIVERY_HOUR:
            notice = Notice_Bot()
            get_nara_bid_info()
            links = get_links_from_db()
            make_csv_file(results=links, filename=csv_file_path)
            
            email_subject = f'[보안 입찰/교육/행사] {today} 주요 정보 요약'
            html = html_template(subject=email_subject, results=links)
            send_email(html, subject=email_subject)
    except Exception as e:
        logger.error(e, exc_info=True)