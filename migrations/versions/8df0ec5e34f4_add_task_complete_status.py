"""add task complete status

Revision ID: 8df0ec5e34f4
Revises: 14c1f3c1661b
Create Date: 2023-07-31 11:49:48.159221

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8df0ec5e34f4'
down_revision = '14c1f3c1661b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status', sa.String(length=10), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.drop_column('status')

    # ### end Alembic commands ###
