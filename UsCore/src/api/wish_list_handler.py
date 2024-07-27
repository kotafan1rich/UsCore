import datetime
import uuid
from typing import Optional

from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from .crud import CRUDTasks
from .schemas import TaskRequestSchema, TaskResponseSchema, WishListResponseSchema
from ..db.session import get_db

wish_list_router = APIRouter()


@wish_list_router.post("/", response_model=TaskResponseSchema)
async def create_task(user_data: TaskRequestSchema, db_session: AsyncSession = Depends(get_db)) -> TaskResponseSchema:
	return await CRUDTasks.create_task(
		text=user_data.text,
		priority=user_data.priority,
		is_finished=user_data.is_finished,
		db_session=db_session
	)


@wish_list_router.get("/", response_model=WishListResponseSchema)
async def get_tasks(
		limit: Optional[int] = None, id: Optional[uuid.UUID] = None,
		text: Optional[str] = None,
		date_from: Optional[datetime.datetime] = None,
		date_to: Optional[datetime.datetime] = None,
		db_session_session: AsyncSession = Depends(get_db)
) -> WishListResponseSchema:
	return await CRUDTasks.get_tasks(
		limit=limit,
		id=id,
		date_from=date_from,
		date_to=date_to,
		text=text,
		db_session=db_session_session
	)


@wish_list_router.delete("/", response_model=WishListResponseSchema)
async def delete_tasks(
		id: Optional[uuid.UUID] = None,
		date_from: Optional[datetime.datetime] = None,
		date_to: Optional[datetime.datetime] = None,
		db_session: AsyncSession = Depends(get_db)
) -> WishListResponseSchema:
	return await CRUDTasks.delete_tasks(
		id=id,
		date_from=date_from,
		date_to=date_to,
		db_session=db_session
	)


@wish_list_router.patch("/", response_model=TaskResponseSchema)
async def update_task(id: uuid.UUID, user_data: TaskRequestSchema, db_session: AsyncSession = Depends(get_db)) -> TaskResponseSchema:
	return await CRUDTasks.update_task(
		id=id,
		text=user_data.text,
		priority=user_data.priority,
		is_finished=user_data.is_finished,
		db_session=db_session
	)
