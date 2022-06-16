"""create adress table

Revision ID: b79d27df4353
Revises: 1f36db6c1c45
Create Date: 2022-06-14 21:46:51.007724

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b79d27df4353'
down_revision = '1f36db6c1c45'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('address',
                    sa.Column('id', sa.Integer, nullable=False, primary_key=True),
                    sa.Column('address1', sa.String, nullable=False),
                    sa.Column('address2', sa.String, nullable=False),
                    sa.Column('city', sa.String, nullable=False),
                    sa.Column('state', sa.String, nullable=False),
                    sa.Column('country', sa.String, nullable=False),
                    sa.Column('postalcode', sa.String, nullable=False))


def downgrade() -> None:
    op.drop_table('address')
