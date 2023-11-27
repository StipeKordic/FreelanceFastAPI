"""create services table

Revision ID: ca06ef845cc1
Revises: 
Create Date: 2023-10-27 11:11:27.884997

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ca06ef845cc1'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('services',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('short_description', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.Column('image_path', sa.String(), nullable=False)
                    )
    pass


def downgrade() -> None:
    op.drop_table('services')
    pass
