import uuid
from datetime import datetime

from typing import Annotated, List, Optional, Union
from fastapi import Path

from pydantic import BaseModel, ConfigDict


class TunedModel(BaseModel):
	model_config = ConfigDict(from_attributes=True)


class TaskResponseSchema(TunedModel):
	id: uuid.UUID
	create_date: datetime
	update_date: datetime
	priority: Annotated[int, Path(ge=0)]
	is_finished: bool
	text: Optional[str]


class TaskRequestSchema(TunedModel):
	priority: Annotated[int, Path(ge=0)] = 0
	text: Optional[str] = None
	is_finished: bool = False


class WishListResponseSchema(TunedModel):
	result: Union[List[TaskResponseSchema], None]


class MediaResponseSchema(TunedModel):
	id: uuid.UUID
	create_date: datetime
	update_date: datetime
	file_path: str
	task_id: Optional[uuid.UUID]
	text: Optional[str]


class MediaListResponseSchema(TunedModel):
	result: Union[List[MediaResponseSchema],  None]
