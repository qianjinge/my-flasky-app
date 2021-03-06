"""initial migration

Revision ID: 1f061cc91f40
Revises: 13b087468b15
Create Date: 2015-11-28 09:13:26.642000

"""

# revision identifiers, used by Alembic.
revision = '1f061cc91f40'
down_revision = '13b087468b15'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('avatar_hash', sa.String(length=32), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'avatar_hash')
    ### end Alembic commands ###
