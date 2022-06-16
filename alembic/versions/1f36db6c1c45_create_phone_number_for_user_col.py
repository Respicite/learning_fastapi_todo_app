"""create phone number for user col

Revision ID: 1f36db6c1c45
Revises: 
Create Date: 2022-06-14 21:36:04.285575

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1f36db6c1c45'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'phone_number')
