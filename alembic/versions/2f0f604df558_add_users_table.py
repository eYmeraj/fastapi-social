"""add users table

Revision ID: 2f0f604df558
Revises: e7676445488b
Create Date: 2023-05-19 16:33:41.657602

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import text



# revision identifiers, used by Alembic.
revision = '2f0f604df558'
down_revision = 'e7676445488b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("users",
                    sa.Column("id", sa.Integer(), nullable=False),
                    sa.Column("email", sa.String(), nullable=False),
                    sa.Column("password", sa.String(), nullable=False),
                    sa.Column("created_on", sa.TIMESTAMP(timezone=True),
                              server_default=text("now()"), nullable=False),
                    sa.PrimaryKeyConstraint("id"),
                    sa.UniqueConstraint("email"))
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
