import trafilatura
from bs4 import BeautifulSoup
import re
import sqlite3
from datetime import datetime

from configs import logger, NOTICE_URLS, DB_FILE, TABLE_NAME

class Notice_Bot:
    def __init__(self, url=None):
        self.logger = logger
        self.urls = NOTICE_URLS

        self._init_db()

        if self.urls:
            self._process_page()

    # --- DB 초기화 ---
    def _init_db(self):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute(f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT,
                kind TEXT,
                href TEXT UNIQUE,
                title TEXT,
                date TEXT,
                scraped_at TEXT
            )
        """)
        conn.commit()
        conn.close()

    def _process_page(self):
        """Fetch HTML, extract content, and filter links."""
        for source in self.urls:
            links = []
            for kind_url in self.urls[source]:
                kind = list(kind_url.keys())[0]
                url = kind_url[kind]
                html = trafilatura.fetch_url(url)
                if not html:
                    self.logger.warning(f"Failed to fetch: {url}")
                    return

                # 1) 링크 추출 및 필터링
                soup = BeautifulSoup(html, 'html.parser')
               
                for tr in soup.find_all('tr'):
                    a_tag = ''
                    title = ''
                    date = ''
                    for td in tr.find_all('td'):
                        text = td.get_text(strip=True)
                        if not a_tag:
                            a_tag = td.find('a', href=True)  # <td> 안에 있는 <a> 태그 찾기
                        if not title and len(text) > 10:
                            title = td.get_text(strip=True)
                        if not date:
                            date = self._get_date(text)
                    if a_tag:
                        filtered = self._filter_href(source, kind, url, a_tag, title, date)
                        if filtered:
                            links.append(filtered)

                # 2) 추출된 내용 DB에서 저장
                saved_links = self._save_links_to_db(links) 

    def _filter_href(self, source, kind, url, a_tag, title, date):
        """Filter hrefs according to rules and return dict if matched."""
        href = a_tag['href']
        # 외부 링크 제외
        if url in href:
            return None

        # 조건: 특정 패턴 + 숫자 포함
        if href.split('&'):
            href = href.split('&')[0]
        if href.startswith('/'):
            url_list = url.split('/')
            url = f'{url_list[0]}//{url_list[2]}'
        return {'source': source, 'kind': kind, 'href': url + href, 'title': title, 'date': date}

    def _save_links_to_db(self, links):
        if not links:
            self.logger.error('No links to save.')
            return

        saved_links = []
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        for link in links:
            try:
                # 동일한 href + text가 있는지 확인
                c.execute(f"""
                    SELECT COUNT(*) FROM {TABLE_NAME} 
                    WHERE source = ? AND kind = ? AND href = ? AND title = ?
                """, (link['source'], link['kind'], link['href'], link['title']))
                exists = c.fetchone()[0]
                if exists == 0:
                    c.execute(f"""
                        INSERT OR IGNORE INTO {TABLE_NAME} (source, kind, href, title, date, scraped_at)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (link['source'], link['kind'], link['href'], link['title'], link['date'], datetime.now().isoformat()))
                    saved_links.append(link)
            except Exception as e:
                self.logger.error(f"DB insert error: {e}")
        conn.commit()
        conn.close() 
        return saved_links

    def get_latest_links(self, limit=10):
        """
        date 최신순으로 limit개 링크를 가져오는 함수
        """
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        try:
            c.execute(f"""
                SELECT source, kind, href, title, date, scraped_at
                FROM {TABLE_NAME}
                ORDER BY date DESC
                LIMIT ?
            """, (limit,))
            rows = c.fetchall()

            # 리스트 딕셔너리로 변환
            links = []
            for row in rows:
                links.append({
                    'source': row[0],
                    'kind': row[1],
                    'href': row[2],
                    'title': row[3],
                    'date': row[4],
                    'scraped_at': row[5]
                })

            return links
        except Exception as e:
            logger.error(f"DB query error: {e}")
            return []
        finally:
            conn.close()


    def _get_date(self, text):
        date = ''
        date_pattern_1 = r"(\d{4})년\s*(\d{1,2})월\s*(\d{1,2})일"
        date_pattern_2 = r"\d{4}-\d{2}-\d{2}"
        match1 = re.search(date_pattern_1, text)
        if match1:
            year, month, day = match1.groups()
            return f'{int(year):04d}-{int(month):02d}-{int(day):02d}'
        else:
            match2 = re.search(date_pattern_2, text)
            if match2:
                return match2.group(0)

