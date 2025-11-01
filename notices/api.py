import requests
from datetime import datetime

from .db import save_links_to_db
from utils import get_date_three_days_ago, get_today
from configs import API_BASE_URL, REQUEST_PATH, API_KEY, SEARCH_KEYWORDS, logger

NUM_ROWS = 200

three_days_ago = get_date_three_days_ago().replace('-', '')
today = get_today().replace('-', '')

def get_nara_bid_info_by_page_no(page_no):
    bid_url = f'{API_BASE_URL}/{REQUEST_PATH}?serviceKey={API_KEY}&pageNo={page_no}&numOfRows={NUM_ROWS}&type=json&bidNtceBgnDt={three_days_ago}0000&bidNtceEndDt={today}2359'
    response = requests.get(bid_url)
    if response.status_code == 200:
        new_data_list = []
        data_list = response.json()['response']['body']['items']
        for i, data in enumerate(data_list):
            date = data['bidNtceDate']
            title = data['bidNtceNm']
            if any(keyword in title for keyword in SEARCH_KEYWORDS):
                new_data = {
                    'source': '나라장터',
                    'kind': data['bsnsDivNm'],
                    'href': data['bidNtceUrl'],
                    'title': data['bidNtceNm'],
                    'date': data['bidNtceDate'],
                    'demand': data['dmndInsttNm'],
                }
                new_data_list.append(new_data)
        return new_data_list, len(data_list)
    else:
        logger.error(f'❌ 오류 발생: {response.status_code}\n {response.text}')
        return [], NUM_ROWS

def get_nara_bid_info():
    links = []
    for i in range(50):
        bid_links, len_bid = get_nara_bid_info_by_page_no(i+1)
        links = links + bid_links
        if len_bid != NUM_ROWS:
            break
    save_links_to_db(links)
    return links

