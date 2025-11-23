from configs import PAGE_DEFAULT

class Page:
    def __init__(self, page, limit=15):
        try:
            self.page = int(page)
        except Exception:
            self.page = 0
        self.per_page = limit
        self.screen_pages = PAGE_DEFAULT['screen_pages']
        self.offset = self.page * self.per_page

    def paginate(self, count=0):
        if count == 0:
            total_pages = 1
        else:
            if count % self.per_page == 0:
                total_pages = int(count / self.per_page)
            else:
                total_pages = int(count / self.per_page) + 1

        if self.page < 0:
            self.page = 0
        elif self.page > total_pages:
            self.page = total_pages

        start_page = self.page // self.screen_pages * self.screen_pages 

        pages = []
        prev_num = start_page - self.screen_pages
        next_num = start_page + self.screen_pages

        if start_page - self.screen_pages >= 0:
            has_prev = True
        else:
            has_prev = False
        if start_page + self.screen_pages >= total_pages:
            has_next = False
        else:
            has_next = True
        if total_pages > self.screen_pages + start_page:
            for i in range(self.screen_pages):
                pages.append(i + start_page)
        elif total_pages < self.screen_pages:
            for i in range(total_pages):
                pages.append(i + start_page)
        else:
            for i in range(total_pages - start_page):
                pages.append(i + start_page)

        paging = {
            'page': self.page,
            'per_page': self.per_page,
            'has_prev': has_prev,
            'has_next': has_next,
            'prev_num': prev_num,
            'next_num': next_num,
            'count': count,
            'offset': self.offset,
            'pages': pages,
            'screen_pages': self.screen_pages,
            'total_pages': total_pages
        }
        return paging