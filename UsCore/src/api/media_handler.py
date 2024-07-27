from datetime import datetime

from .crud import CRUDMedia
from .schemas import MediaListResponseSchema, MediaResponseSchema

import uuid
from typing import Optional
from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.session import get_db

media_router = APIRouter()


@media_router.post("/", response_model=MediaResponseSchema)
async def upload_media(
		file: UploadFile,
		text: Optional[str] = None,
		task_id: Optional[uuid.UUID] = None,
		db_session: AsyncSession = Depends(get_db)
) -> MediaResponseSchema:
	return await CRUDMedia.upload_media(file=file, task_id=task_id, text=text, db_session=db_session)


@media_router.get("/", response_model=MediaListResponseSchema)
async def get_media(
		id: Optional[uuid.UUID] = None,
		task_id: Optional[uuid.UUID] = None,
		date_from: Optional[datetime] = None,
		date_to: Optional[datetime] = None,
		text: Optional[str] = None,
		db_session: AsyncSession = Depends(get_db)
) -> MediaListResponseSchema:
	return await CRUDMedia.get_media(id, task_id, date_from, date_to, text, db_session)


@media_router.patch("/", response_model=MediaResponseSchema)
async def update_media(
		id: uuid.UUID, file: UploadFile = None,
		task_id: Optional[uuid.UUID] = None,
		text: Optional[str] = None,
		db_session: AsyncSession = Depends(get_db)
) -> MediaResponseSchema:
	return await CRUDMedia.update_media(id, file, task_id, text, db_session)


@media_router.delete("/", response_model=MediaListResponseSchema)
async def delete_media(
		id: Optional[uuid.UUID] = None,
		date_from: Optional[datetime] = None,
		date_to: Optional[datetime] = None,
		db_session: AsyncSession = Depends(get_db)
) -> MediaListResponseSchema:
	return await CRUDMedia.delete_media(id, date_from, date_to, db_session)
