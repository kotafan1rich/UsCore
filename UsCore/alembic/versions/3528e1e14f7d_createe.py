"""createe

Revision ID: 3528e1e14f7d
Revises: dd3d12f743cb
Create Date: 2024-07-25 17:36:11.574311

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3528e1e14f7d'
down_revision: Union[str, None] = 'dd3d12f743cb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('wishlists',
    sa.Column('priority', sa.INTEGER(), nullable=True),
    sa.Column('is_finished', sa.BOOLEAN(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('create_date', sa.DateTime(timezone=True), nullable=False),
    sa.Column('update_date', sa.DateTime(timezone=True), nullable=False),
    sa.Column('text', sa.VARCHAR(length=1000), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('media',
    sa.Column('file_path', sa.String(length=200), nullable=True),
    sa.Column('task_id', sa.UUID(), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('create_date', sa.DateTime(timezone=True), nullable=False),
    sa.Column('update_date', sa.DateTime(timezone=True), nullable=False),
    sa.Column('text', sa.VARCHAR(length=1000), nullable=True),
    sa.ForeignKeyConstraint(['task_id'], ['wishlists.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('media')
    op.drop_table('wishlists')
    # ### end Alembic commands ###
