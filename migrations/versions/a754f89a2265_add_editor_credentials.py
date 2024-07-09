"""Add editor credentials

Revision ID: a754f89a2265
Revises: 1cf4a812dcda
Create Date: 2024-07-06 11:45:46.307516

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a754f89a2265'
down_revision = '1cf4a812dcda'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('editor_username', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('editor_password', sa.String(length=100), nullable=True))
        batch_op.create_unique_constraint('uq_user_editor_username', ['editor_username'])


def downgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint('uq_user_editor_username', type_='unique')
        batch_op.drop_column('editor_username')
        batch_op.drop_column('editor_password')
