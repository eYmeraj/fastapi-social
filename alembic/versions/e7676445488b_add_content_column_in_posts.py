"""add content column in posts

Revision ID: e7676445488b
Revises: cef8691d1d14
Create Date: 2023-05-19 16:29:28.993671

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7676445488b'
down_revision = 'cef8691d1d14'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
