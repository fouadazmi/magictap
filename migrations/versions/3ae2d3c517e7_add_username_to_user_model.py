"""Add username to User model

Revision ID: 3ae2d3c517e7
Revises: a754f89a2265
Create Date: 2024-07-08 14:35:00.123456

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ae2d3c517e7'
down_revision = 'a754f89a2265'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.String(length=100), nullable=False))
        batch_op.create_unique_constraint('uq_user_username', ['username'])  # Add a name for the unique constraint


def downgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint('uq_user_username', type_='unique')
        batch_op.drop_column('username')
