"""use fullname

Revision ID: 1babbfdcff16
Revises: None
Create Date: 2013-11-21 09:43:15.388377

"""

# revision identifiers, used by Alembic.
revision = '1babbfdcff16'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    print "helo"
    op.add_column('users', sa.Column('fullname', sa.String(101)))


def downgrade():
    op.drop_column('users', 'fullname')
