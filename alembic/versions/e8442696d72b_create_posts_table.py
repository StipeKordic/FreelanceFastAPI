"""create posts table

Revision ID: e8442696d72b
Revises: 423baf2415ca
Create Date: 2023-10-27 12:01:43.911402

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e8442696d72b'
down_revision: Union[str, None] = '423baf2415ca'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('service_id', sa.Integer(), nullable=False),
                    sa.Column('description', sa.String(), nullable=False),
                    sa.Column('price', sa.Float(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.Column('image_path', sa.String(), nullable=False)
                    )
    op.create_foreign_key('posts_users_fk', source_table="posts", referent_table="users",
                          local_cols=['user_id'], remote_cols=['id'], ondelete="CASCADE")
    op.create_foreign_key('posts_services_fk', source_table="posts", referent_table="services",
                          local_cols=['service_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
