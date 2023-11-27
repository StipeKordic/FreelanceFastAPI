"""create token blacklist table

Revision ID: eebf47021a9e
Revises: 5117a2c42886
Create Date: 2023-11-09 11:52:51.952887

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eebf47021a9e'
down_revision: Union[str, None] = '5117a2c42886'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('token_blacklist',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('token', sa.String(), nullable=False),
                    sa.Column('logout_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    )
    pass
    pass


def downgrade() -> None:
    op.drop_table('token_blacklist')
    pass
