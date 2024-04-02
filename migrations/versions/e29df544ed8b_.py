"""empty message

Revision ID: e29df544ed8b
Revises: 14d6eb6220da
Create Date: 2024-03-17 14:45:03.621340

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e29df544ed8b'
down_revision = '14d6eb6220da'
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
