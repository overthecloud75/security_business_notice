from fastapi import APIRouter, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from notices import get_links_from_db, get_total_count
from utils import Page
from configs import logger, BUSINESS_COLUMN_HEADER, PAGE_DEFAULT


templates = Jinja2Templates(directory='templates')

router = APIRouter(
    prefix='',
)

@router.get('/favicon.ico')
async def favicon():
    return Response(status_code=204)

@router.get('/', response_class=HTMLResponse)
async def index(request: Request, page: int = 0, limit: int = PAGE_DEFAULT['per_page'], search: str = ''):
    try:
        column_header = BUSINESS_COLUMN_HEADER
        count = get_total_count(search=search)
        links = get_links_from_db(limit=limit, page=page)
        page_object = Page(page=page, limit=limit)
        paging = page_object.paginate(count=count)
        links = get_links_from_db(limit=limit, page=page, search=search)
        return templates.TemplateResponse(
            'dashboard.html', 
            {'request': request, 'data_list': links, 'update_title': '보안 비즈니스 공지', 'column_header': BUSINESS_COLUMN_HEADER, 'paging': paging, 'search': search}
        )
    except Exception as e:
        logger.error(e, exc_info=True)
        return ''