"""create adress_id to users

Revision ID: 39090e73b737
Revises: b79d27df4353
Create Date: 2022-06-14 21:55:05.514900

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '39090e73b737'
down_revision = 'b79d27df4353'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('address_id', sa.Integer, nullable=True))
    op.create_foreign_key('address_users_fk', source_table='users', referent_table='address',
                          local_cols=['address_id'], remote_cols=['id'], ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint('address_users_fk', table_name='users')
    op.drop_column('users' 'address_id')
