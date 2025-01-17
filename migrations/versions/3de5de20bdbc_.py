"""empty message

Revision ID: 3de5de20bdbc
Revises: 
Create Date: 2024-02-06 14:09:39.135120

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '3de5de20bdbc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('t_duty_plan', sa.Column('staff_code', sa.String(length=64), nullable=True))
    op.drop_constraint('t_duty_plan_ibfk_2', 't_duty_plan', type_='foreignkey')
    op.create_foreign_key(None, 't_duty_plan', 't_staff', ['staff_code'], ['staff_code'])
    op.drop_column('t_duty_plan', 'duty_staff_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('t_duty_plan', sa.Column('duty_staff_id', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 't_duty_plan', type_='foreignkey')
    op.create_foreign_key('t_duty_plan_ibfk_2', 't_duty_plan', 't_staff', ['duty_staff_id'], ['staff_id'])
    op.drop_column('t_duty_plan', 'staff_code')
    # ### end Alembic commands ###
