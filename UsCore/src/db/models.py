import uuid

from datetime import datetime, timedelta, timezone

from sqlalchemy import INTEGER, String, VARCHAR, Column, DateTime, ForeignKey, BOOLEAN
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship

from src.db.session import metadata

Base = declarative_base(metadata=metadata)


class UsCoreCommonModel:
	id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
	create_date = Column(DateTime(), default=datetime.now(), nullable=False)
	update_date = Column(DateTime(), default=datetime.now(), onupdate=datetime.now(), nullable=False)
	text = Column(VARCHAR(length=1000), nullable=True)


class WishListModel(Base, UsCoreCommonModel):
	__tablename__ = 'wishlists'

	priority = Column(INTEGER, nullable=True)
	is_finished = Column(BOOLEAN, default=False, nullable=False)
	media = relationship('MediaModel', back_populates='wishlist')


class MediaModel(Base, UsCoreCommonModel):
	__tablename__ = 'media'

	file_path = Column(String(200), nullable=True)
	task_id = Column(UUID(as_uuid=True), ForeignKey(WishListModel.id, ondelete='SET NULL'), nullable=True)
	wishlist = relationship('WishListModel', back_populates='media')
