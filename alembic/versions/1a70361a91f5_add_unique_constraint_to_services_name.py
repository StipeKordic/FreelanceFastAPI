"""add unique constraint to services name

Revision ID: 1a70361a91f5
Revises: eebf47021a9e
Create Date: 2024-01-24 14:01:10.632499

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1a70361a91f5'
down_revision: Union[str, None] = 'eebf47021a9e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint('unique_constraint_name_services', 'services', ['name'])
    pass


def downgrade() -> None:
    op.drop_constraint('unique_constraint_name_services', 'services')
    pass
