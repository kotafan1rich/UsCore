import uuid
from datetime import datetime
from typing import Optional, Union
from fastapi.exceptions import HTTPException
from fastapi import UploadFile

from .schemas import MediaListResponseSchema, TaskResponseSchema, WishListResponseSchema, MediaResponseSchema

from sqlalchemy.ext.asyncio import AsyncSession

from ..db.dals import MediaDAL, WishListDAL
from ..db.models import MediaModel
from ..settings import MEDIA_PATH


class CRUDTasks:
	@staticmethod
	async def create_task(text: Union[str, None], priority: int, is_finished: bool, db_session: AsyncSession) -> TaskResponseSchema:
		wishlist_dal = WishListDAL(db_session=db_session)
		task = await wishlist_dal.create_task(
			text=text,
			priority=priority,
			is_fineshed=is_finished
		)
		return TaskResponseSchema.model_validate(task, from_attributes=True)

	@staticmethod
	async def get_tasks(limit: Optional[int], id: Optional[uuid.UUID], text: Optional[str], date_from: Optional[datetime], date_to: Optional[datetime], db_session: AsyncSession) -> WishListResponseSchema:

		wishlist_dal = WishListDAL(db_session=db_session)
		tasks = await wishlist_dal.get_tasks(limit=limit, id=id, text=text, date_from=date_from, date_to=date_to)
		if not tasks:
			raise HTTPException(status_code=404, detail="No tasks found")
		tasks_schema = [TaskResponseSchema.model_validate(task, from_attributes=True) for task in tasks]
		return WishListResponseSchema(result=tasks_schema)

	@staticmethod
	async def delete_tasks(id: Optional[uuid.UUID], date_from: Optional[datetime], date_to: Optional[datetime], db_session: AsyncSession) -> WishListResponseSchema:

		wishlist_dal = WishListDAL(db_session=db_session)
		deleted_tasks = await wishlist_dal.delete_task(id=id, date_from=date_from, date_to=date_to)
		tasks_schema = [TaskResponseSchema.model_validate(task, from_attributes=True) for task in deleted_tasks]
		return WishListResponseSchema(result=tasks_schema)

	@staticmethod
	async def update_task(id: uuid.UUID, text: Optional[str], priority: int, is_finished: Optional[bool], db_session: AsyncSession) -> TaskResponseSchema:

		wishlist_dal = WishListDAL(db_session=db_session)
		updated_task = await wishlist_dal.update_task(id=id, text=text, priority=priority, is_finised=is_finished)
		return TaskResponseSchema.model_validate(updated_task, from_attributes=True)


class CRUDMedia:
	@staticmethod
	async def upload_media(file: UploadFile, task_id: Optional[uuid.UUID], text: Optional[str], db_session: AsyncSession) -> MediaResponseSchema:
		file_path = f"{MEDIA_PATH}/images/{file.filename}"

		media_dal = MediaDAL(db_session=db_session)
		media: MediaModel = await media_dal.upload_media(file=file, text=text, task_id=task_id, file_path=file_path)
		return MediaResponseSchema.model_validate(media, from_attributes=True)

	@staticmethod
	async def get_media(id: Optional[uuid.UUID], task_id: Optional[uuid.UUID], date_from: Optional[datetime], date_to: Optional[datetime], text: Optional[str], db_session: AsyncSession) -> MediaListResponseSchema:

		media_dal = MediaDAL(db_session=db_session)
		medias = await media_dal.get_media(id=id, task_id=task_id, date_from=date_from, date_to=date_to, text=text)
		if not medias:
			raise HTTPException(status_code=404, detail="No medias found")
		media_schema = [MediaResponseSchema.model_validate(media, from_attributes=True) for media in medias]
		return MediaListResponseSchema(result=media_schema)

	@staticmethod
	async def update_media(id: Optional[uuid.UUID], file: Optional[UploadFile], task_id: Optional[uuid.UUID], text: Optional[str], db_session: AsyncSession) -> MediaResponseSchema:
		file_path = f"{MEDIA_PATH}/images/{file.filename}" if file else None
		media_dal = MediaDAL(db_session=db_session)
		updated_media: MediaModel = await media_dal.update_media(id=id, task_id=task_id, text=text, file_path=file_path, file=file)
		if not updated_media:
			raise HTTPException(status_code=404, detail="No medias found")
		return MediaResponseSchema.model_validate(updated_media, from_attributes=True)

	@staticmethod
	async def delete_media(
			id: Optional[uuid.UUID],
			date_from: Optional[datetime],
			date_to: Optional[datetime],
			db_session: AsyncSession
	) -> MediaListResponseSchema:
		media_dal = MediaDAL(db_session=db_session)
		deleted_media = await media_dal.delete_media(id=id, date_from=date_from, date_to=date_to)
		media_schema = [MediaResponseSchema.model_validate(media, from_attributes=True) for media in deleted_media]
		return MediaListResponseSchema(result=media_schema)
