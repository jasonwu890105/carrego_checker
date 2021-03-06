"""carss table

Revision ID: 059677344d73
Revises: 
Create Date: 2018-12-17 18:01:55.761161

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '059677344d73'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cars',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('regonum', sa.String(length=15), nullable=False),
    sa.Column('driver', sa.String(length=50), nullable=True),
    sa.Column('state', sa.String(length=20), nullable=False),
    sa.Column('manager', sa.String(length=50), nullable=False),
    sa.Column('expirydate', sa.DateTime(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cars_driver'), 'cars', ['driver'], unique=False)
    op.create_index(op.f('ix_cars_regonum'), 'cars', ['regonum'], unique=True)
    op.create_index(op.f('ix_cars_state'), 'cars', ['state'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_cars_state'), table_name='cars')
    op.drop_index(op.f('ix_cars_regonum'), table_name='cars')
    op.drop_index(op.f('ix_cars_driver'), table_name='cars')
    op.drop_table('cars')
    # ### end Alembic commands ###
