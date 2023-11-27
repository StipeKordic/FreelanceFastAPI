"""create_userRoles_table

Revision ID: 0f23fff63892
Revises: cad7a26b08e7
Create Date: 2023-11-07 13:57:11.528226

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0f23fff63892'
down_revision: Union[str, None] = 'cad7a26b08e7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('user_roles',
                    sa.Column('user_id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('role_id', sa.Integer(), nullable=False, primary_key=True),
                    )
    op.create_foreign_key('userrole_user_fk', source_table="user_roles", referent_table="users",
                          local_cols=['user_id'], remote_cols=['id'], ondelete="CASCADE")
    op.create_foreign_key('userrole_role_fk', source_table="user_roles", referent_table="roles",
                          local_cols=['role_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_table('user_roles')
    pass
