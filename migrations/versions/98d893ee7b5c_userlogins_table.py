"""userlogins table

Revision ID: 98d893ee7b5c
Revises: 493f0f84d016
Create Date: 2019-01-09 23:16:43.166469

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '98d893ee7b5c'
down_revision = '493f0f84d016'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('userlogin',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_userlogin_email'), 'userlogin', ['email'], unique=True)
    op.create_index(op.f('ix_userlogin_username'), 'userlogin', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_userlogin_username'), table_name='userlogin')
    op.drop_index(op.f('ix_userlogin_email'), table_name='userlogin')
    op.drop_table('userlogin')
    # ### end Alembic commands ###
