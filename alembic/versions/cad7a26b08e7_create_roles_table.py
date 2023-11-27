"""create_roles_table

Revision ID: cad7a26b08e7
Revises: 76db70461492
Create Date: 2023-11-07 13:20:32.796667

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cad7a26b08e7'
down_revision: Union[str, None] = '76db70461492'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('roles',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('role_name', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    )
    pass


def downgrade() -> None:
    op.drop_table('roles')
    pass
