import os

if os.environ.get('PRODUCTION_MODE'):
    PRODUCTION_MODE = True # Release를 의미 
else:
    PRODUCTION_MODE = False 

# SQLite
LOG_DIR = 'database'
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)

DB_FILE = 'database/links.db'
TABLE_NAME = 'links'

# csv
CSV_DIR = 'csv'
if not os.path.exists(CSV_DIR):
    os.mkdir(CSV_DIR)

# URL
NOTICE_URLS = {
    'kisia': [
        {'알림': 'https://www.kisia.or.kr/announcement/association/'},
        {'행사': 'https://www.kisia.or.kr/announcement/relative/'},
        {'교육': 'https://www.kisia.or.kr/talent_support/education_apply/reference/'}

    ], 
    'kisa': [
        {'입찰': 'https://www.kisa.or.kr/403'}
    ]
}

# 나라장터 API
API_BASE_URL = 'https://apis.data.go.kr/1230000/ao/PubDataOpnStdService'
REQUEST_PATH = '/getDataSetOpnStdBidPblancInfo'
SEARCH_KEYWORDS = ['사이버보안', '사이버 보안', '모의해킹', '모의침투', '취약점', '보안장비', '침해사고']

# etc
DELIVERY_HOUR = 11