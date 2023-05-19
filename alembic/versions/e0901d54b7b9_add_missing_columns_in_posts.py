"""add missing columns in posts

Revision ID: e0901d54b7b9
Revises: 6f9b3a0b8f43
Create Date: 2023-05-19 16:45:35.206861

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e0901d54b7b9'
down_revision = '6f9b3a0b8f43'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column('published', sa.Boolean(), nullable=False, server_default="TRUE"))
    op.add_column("posts", sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")))              
    pass


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
