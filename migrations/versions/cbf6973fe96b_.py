"""empty message

Revision ID: cbf6973fe96b
Revises: 10e8bdfa02a6
Create Date: 2024-03-17 18:29:31.871742

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cbf6973fe96b'
down_revision = '10e8bdfa02a6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('t_other_setting',
    sa.Column('other_id', sa.Integer(), nullable=False),
    sa.Column('other_setting_key', sa.String(length=64), nullable=True),
    sa.Column('other_setting_value', sa.String(length=64), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('other_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('t_other_setting')
    # ### end Alembic commands ###
