"""initial migration

Revision ID: c1062934337
Revises: 3fef90587ca5
Create Date: 2015-11-25 18:29:52.151000

"""

# revision identifiers, used by Alembic.
revision = 'c1062934337'
down_revision = '3fef90587ca5'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password_hash', sa.String(length=128), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'password_hash')
    ### end Alembic commands ###