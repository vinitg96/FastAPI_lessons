"""add content column to post table

Revision ID: 129555b1c7d6
Revises: 9e7c4381ebcb
Create Date: 2025-03-04 12:34:06.812566

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '129555b1c7d6'
down_revision: Union[str, None] = '9e7c4381ebcb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content',sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
