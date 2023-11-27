"""create permissions table

Revision ID: 6513b3ff3529
Revises: 0f23fff63892
Create Date: 2023-11-08 09:03:12.176967

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6513b3ff3529'
down_revision: Union[str, None] = '0f23fff63892'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('permissions',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('permission_name', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    )
    pass


def downgrade() -> None:
    op.drop_table('permissions')
    pass
