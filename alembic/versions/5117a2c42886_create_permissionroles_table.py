"""create permissionroles table

Revision ID: 5117a2c42886
Revises: 6513b3ff3529
Create Date: 2023-11-08 09:08:19.054781

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5117a2c42886'
down_revision: Union[str, None] = '6513b3ff3529'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('permission_roles',
                    sa.Column('permission_id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('role_id', sa.Integer(), nullable=False, primary_key=True),
                    )
    op.create_foreign_key('permissionrole_permission_fk', source_table="permission_roles", referent_table="permissions",
                          local_cols=['permission_id'], remote_cols=['id'], ondelete="CASCADE")
    op.create_foreign_key('permissionrole_role_fk', source_table="permission_roles", referent_table="roles",
                          local_cols=['role_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_table('permission_roles')
    pass
