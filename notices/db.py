import sqlite3
from datetime import datetime

from configs import DB_FILE, TABLE_NAME, logger


def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,
            kind TEXT,
            href TEXT UNIQUE,
            title TEXT,
            demand TEXT,
            date TEXT,
            scraped_at TEXT
        )
    """)
    c.execute(f"CREATE INDEX IF NOT EXISTS idx_{TABLE_NAME}_date_title ON {TABLE_NAME}(date, title)")
     # source, kind, href, title 컬럼 복합 인덱스 생성
    c.execute(f"""
        CREATE INDEX IF NOT EXISTS idx_{TABLE_NAME}_source_kind_href_title
        ON {TABLE_NAME}(source, kind, href, title)
    """)
    conn.commit()
    conn.close()

def save_links_to_db(links):
    if not links:
        logger.error('No links to save.')
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
                    INSERT OR IGNORE INTO {TABLE_NAME} (source, kind, href, title, demand, date, scraped_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (link['source'], link['kind'], link['href'], link['title'], link['demand'], link['date'], datetime.now().isoformat()))
                saved_links.append(link)
        except Exception as e:
            logger.error(f"DB insert error: {e}")
    conn.commit()
    conn.close() 
    return saved_links

def get_links_from_db(limit=30, page=0, search=''):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    offset = page * limit
    try:
        if search and len(search) > 1:
            # search가 있는 경우
            query = f"""
                SELECT source, kind, href, title, demand, date, scraped_at
                FROM {TABLE_NAME}
                WHERE title LIKE ?
                ORDER BY date DESC, title ASC
                LIMIT ? OFFSET ?
            """
            params = (f'%{search}%', limit, offset)
        else:
            # search가 없는 경우
            query = f"""
                SELECT source, kind, href, title, demand, date, scraped_at
                FROM {TABLE_NAME}
                ORDER BY date DESC, title ASC
                LIMIT ? OFFSET ?
            """
            params = (limit, offset)

        c.execute(query, params)
        rows = c.fetchall()

        # 리스트 딕셔너리로 변환
        links = []
        for row in rows:
            links.append({
                'source': row[0],
                'kind': row[1],
                'href': row[2],
                'title': row[3],
                'demand': row[4],
                'date': row[5],
                'scraped_at': row[6]
            })
        return links
    except Exception as e:
        logger.error(f'DB query error: {e}')
        return []
    finally:
        conn.close()

def get_total_count(search=''):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    try:
        if search and len(search) > 1:
            query = f"SELECT COUNT(*) FROM {TABLE_NAME} WHERE title LIKE ?"
            params = (f'%{search}%',)
            c.execute(query, params)
        else:
            query = f"SELECT COUNT(*) FROM {TABLE_NAME}"
            c.execute(query)
        
        total_count = c.fetchone()[0] 
        return total_count

    except Exception as e:
        logger.error(f'DB count error: {e}')
        return 0

    finally:
        conn.close()
