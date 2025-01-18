"""empty message

Revision ID: 882b5c4a7ee0
Revises: 29b0f3e178bd
Create Date: 2025-01-17 01:48:14.519563

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '882b5c4a7ee0'
down_revision = '29b0f3e178bd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('patient', schema=None) as batch_op:
        batch_op.add_column(sa.Column('token', sa.Integer(), nullable=False))
        batch_op.create_unique_constraint(None, ['token'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('patient', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('token')

    # ### end Alembic commands ###
