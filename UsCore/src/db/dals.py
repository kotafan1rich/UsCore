import uuid
from datetime import datetime
from typing import Optional
from aiofiles import open as aio_open
from aiofiles.os import remove as aio_remove
from aiofiles.ospath import exists as aio_exists
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.exceptions import HTTPException
from fastapi import UploadFile

from src.db.models import MediaModel, WishListModel


def get_default_get_query(text: Optional[str], date_from: Optional[datetime], date_to: Optional[datetime], model):
    query = select(model)
    if date_from is not None:
        query = query.filter(model.create_date >= date_from)
    if date_to is not None:
        query = query.filter(model.create_date <= date_to)
    if text is not None:
        query = query.filter(model.text.ilike(f'%{text}%'))
    return query


class WishListDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_task(self, text: Optional[str], priority: int, is_fineshed: bool) -> WishListModel:
        new_task = WishListModel(
            text=text,
            priority=priority,
            is_finished=is_fineshed,
        )

        self.db_session.add(new_task)
        await self.db_session.commit()
        return new_task

    async def get_tasks(self, limit: Optional[int], id: Optional[uuid.UUID], text: Optional[str], date_from: Optional[datetime], date_to: Optional[datetime]):
        if id is None:
            query = get_default_get_query(text, date_from, date_to, WishListModel)
            if limit is not None:
                query = query.order_by(WishListModel.create_date.desc()).limit(limit)

            result = await self.db_session.execute(query)
            return result.scalars().all()
        query = select(WishListModel).where(id == WishListModel.id)
        result = await self.db_session.execute(query)
        return result.fetchone()

    async def delete_task(self, id: Optional[uuid.UUID], date_from: Optional[datetime], date_to: Optional[datetime]):
        query = select(WishListModel)
        if id is None:
            if date_from is not None:
                query = query.filter(WishListModel.create_date >= date_from)
            if date_to is not None:
                query = query.filter(WishListModel.create_date <= date_to)
        else:
            query = query.where(id == WishListModel.id)

        res = await self.db_session.execute(query)
        tasks = res.scalars().all()

        if not tasks:
            raise HTTPException(status_code=404, detail="No tasks found")
        for task in tasks:
            await self.db_session.delete(task)

        await self.db_session.commit()
        return tasks

    async def update_task(self, id: uuid.UUID, text: Optional[str], priority: int, is_finised: Optional[bool]) -> WishListModel:
        query = select(WishListModel).where(id == WishListModel.id)
        result = await self.db_session.execute(query)
        task: WishListModel = result.scalar_one_or_none()
        if not task:
            raise HTTPException(status_code=404, detail="No task found")

        task.text = text
        task.priority = priority
        task.is_finished = is_finised

        await self.db_session.commit()
        await self.db_session.refresh(task)

        return task


class MediaDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def upload_media(self, file, text: Optional[str], task_id: Optional[uuid.UUID], file_path: str):
        new_media = MediaModel(
            file_path=file_path,
            task_id=task_id,
            text=text,
        )

        self.db_session.add(new_media)
        await self.db_session.commit()

        async with aio_open(file_path, "wb+") as buffer:
            await buffer.write(await file.read())

        return new_media

    async def get_media(self, id: Optional[uuid.UUID], task_id: Optional[uuid.UUID], date_from: Optional[datetime], date_to: Optional[datetime], text: Optional[str]):
        if id is None:
            query = get_default_get_query(text, date_from, date_to, MediaModel)

            if task_id is not None:
                query = query.filter(task_id == MediaModel.task_id)

            result = await self.db_session.execute(query)
            return result.scalars().all()

        query = select(MediaModel).where(id == MediaModel.id)
        result = await self.db_session.execute(query)
        return result.fetchone()

    async def update_media(self, id: Optional[uuid.UUID], task_id: Optional[uuid.UUID], text: Optional[str], file_path: str, file: Optional[UploadFile]):
        query = select(MediaModel).where(id == MediaModel.id)
        result = await self.db_session.execute(query)
        media: MediaModel = result.scalar_one_or_none()

        if not media:
            raise HTTPException(status_code=404, detail="No media found")

        media.text = text
        media.task_id = task_id

        if file:
            if await aio_exists(media.file_path):
                await aio_remove(media.file_path)

            async with aio_open(file_path, "wb+") as buffer:
                await buffer.write(await file.read())

            media.file_path = file_path

        await self.db_session.commit()
        await self.db_session.refresh(media)

        return media

    async def delete_media(self, id: Optional[uuid.UUID], date_from: Optional[datetime], date_to: Optional[datetime]):
        query = select(MediaModel)
        if id is None:
            if date_from is not None:
                query = query.filter(MediaModel.create_date >= date_from)
            if date_to is not None:
                query = query.filter(MediaModel.create_date <= date_to)
        else:
            query = query.where(id == MediaModel.id)

        res = await self.db_session.execute(query)
        medias = res.scalars().all()

        if not medias:
            raise HTTPException(status_code=404, detail="No media found")
        for media in medias:
            await self.db_session.delete(media)

        await self.db_session.commit()
        return medias
