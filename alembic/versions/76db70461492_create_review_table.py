"""create review table

Revision ID: 76db70461492
Revises: e3a4e48995d7
Create Date: 2023-10-27 13:24:58.933058

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '76db70461492'
down_revision: Union[str, None] = 'e8442696d72b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('reviews',
                    sa.Column('user_id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('post_id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('review', sa.Float(), nullable=False)
                    )
    op.create_foreign_key('review_user_fk', source_table="reviews", referent_table="users",
                          local_cols=['user_id'], remote_cols=['id'], ondelete="CASCADE")
    op.create_foreign_key('review_post_fk', source_table="reviews", referent_table="posts",
                          local_cols=['post_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_table('reviews')
    pass
