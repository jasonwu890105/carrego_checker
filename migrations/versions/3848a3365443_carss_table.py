"""carss table

Revision ID: 3848a3365443
Revises: 
Create Date: 2019-02-23 20:46:30.119561

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3848a3365443'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cars', sa.Column('email_sent', sa.String(length=200), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('cars', 'email_sent')
    # ### end Alembic commands ###