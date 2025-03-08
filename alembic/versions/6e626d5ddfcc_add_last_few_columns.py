"""Add Last Few Columns

Revision ID: 6e626d5ddfcc
Revises: 3359e1edbb1f
Create Date: 2025-03-08 12:43:09.872778

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6e626d5ddfcc'
down_revision: Union[str, None] = '3359e1edbb1f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE')
        )
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()'))
    )



def downgrade() -> None:
    op.drop_column('posts', column_name='published')
    op.drop_column('posts', 'created_at' )
