"""empty message

Revision ID: 10e8bdfa02a6
Revises: c586e2541ae6
Create Date: 2024-03-17 15:01:13.833108

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '10e8bdfa02a6'
down_revision = 'c586e2541ae6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('t_place', sa.Column('is_deleted', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('t_place', 'is_deleted')
    # ### end Alembic commands ###
