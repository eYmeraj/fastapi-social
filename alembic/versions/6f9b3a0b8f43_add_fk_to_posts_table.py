"""add fk to posts table

Revision ID: 6f9b3a0b8f43
Revises: 2f0f604df558
Create Date: 2023-05-19 16:41:01.612156

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6f9b3a0b8f43'
down_revision = '2f0f604df558'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("user_id", sa.Integer(), nullable=False))

    op.create_foreign_key("posts_users_fk", 
                          source_table="posts", 
                          referent_table="users", 
                          local_cols= ["user_id"],
                          remote_cols=["id"],
                          ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint("posts_users_fk", table_name="posts")
    op.drop_column("posts", "user_id")
    pass
