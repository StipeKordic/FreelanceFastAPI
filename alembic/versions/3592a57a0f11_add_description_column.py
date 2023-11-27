"""add description column

Revision ID: 3592a57a0f11
Revises: ca06ef845cc1
Create Date: 2023-10-27 11:18:03.081900

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3592a57a0f11'
down_revision: Union[str, None] = 'ca06ef845cc1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('services', sa.Column('description', sa.Text(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('services', 'description')
    pass
