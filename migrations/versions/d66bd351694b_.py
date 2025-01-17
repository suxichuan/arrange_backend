"""empty message

Revision ID: d66bd351694b
Revises: 89336005fbe7
Create Date: 2024-03-17 14:43:21.428969

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd66bd351694b'
down_revision = '89336005fbe7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('t_place', 'is_deleted')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('t_place', sa.Column('is_deleted', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
