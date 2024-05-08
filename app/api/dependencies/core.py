from multiprocessing import Queue
from typing import Annotated
from app.scrap_queue import get_webscrap_queue

from app.database import get_db_session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

DBSessionDep = Annotated[AsyncSession, Depends(get_db_session)]


