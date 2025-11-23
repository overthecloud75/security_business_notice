import time
import threading
import uvicorn
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from domain.main import main_router
from configs import logger
from business_notice import business_notice


# 1. 스레드 제어를 위한 전역 변수: 종료 신호를 보낼 이벤트 객체
stop_event = threading.Event()

def background_worker():
    counter = 0
    while not stop_event.is_set():
        counter += 1
        business_notice()
        stop_event.wait(3600) 

@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 생명 주기 관리 함수"""

    # === 🚀 서버 시작 (Startup) 시점 ===
    global worker_thread
    worker_thread = threading.Thread(target=background_worker)
    worker_thread.start() # 스레드 실행
    
    print('✅ [Main] FastAPI 애플리케이션 시작 완료.')
    # yield: 이 시점을 기준으로 웹 서버가 요청을 받기 시작합니다.
    yield 
    
    # === 🛑 서버 종료 (Shutdown) 시점 ===
    print('⏳ [Main] 서버 종료 시작... 백그라운드 워커 정리 중.')
    
    stop_event.set()      # 워커 스레드에 종료하라는 신호 전달
    worker_thread.join()  # 워커 스레드가 작업을 완료하고 완전히 종료될 때까지 대기 (안전한 종료 보장)

    print('🛑 [Main] 백그라운드 워커 및 FastAPI 종료 완료.')

# lifespan을 FastAPI 인스턴스에 전달
app = FastAPI(lifespan=lifespan)

static_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
if os.path.isdir(static_root):
    app.mount('/static', StaticFiles(directory=static_root), name='static')
else:
    logger.warning(f'Static directory not found: {static_root}')

app.include_router(main_router.router)
