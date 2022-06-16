"""create apt_num for address col

Revision ID: 6ea33f4e9eba
Revises: 39090e73b737
Create Date: 2022-06-16 17:40:22.460720

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6ea33f4e9eba'
down_revision = '39090e73b737'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('address', sa.Column('apt_num', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('address', 'apt_num')