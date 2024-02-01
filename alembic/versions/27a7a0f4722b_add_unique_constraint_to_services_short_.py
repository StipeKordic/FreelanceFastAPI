"""add unique constraint to services short description

Revision ID: 27a7a0f4722b
Revises: 1a70361a91f5
Create Date: 2024-01-31 12:44:32.211153

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '27a7a0f4722b'
down_revision: Union[str, None] = '1a70361a91f5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint('unique_constraint_short_description_services', 'services', ['short_description'])
    pass


def downgrade() -> None:
    op.drop_constraint('unique_constraint_short_description_services', 'services')
    pass
