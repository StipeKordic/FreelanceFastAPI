"""create chatboxes table

Revision ID: 7ed61bd579fa
Revises: 27a7a0f4722b
Create Date: 2024-02-16 12:36:21.397834

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7ed61bd579fa'
down_revision: Union[str, None] = '27a7a0f4722b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('chatboxes',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    )
    op.create_foreign_key('chatbox_user_fk', source_table="chatboxes", referent_table="users",
                          local_cols=['user_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_table('chatboxes')
    pass
