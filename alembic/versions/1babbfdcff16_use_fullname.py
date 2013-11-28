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
    print "Adding fullname column"
    op.add_column('users', sa.Column('fullname', sa.String(101)))
    
    print "Merging firstname + lastname into fullname"
    connection = op.get_bind()
    connection.execute("update users set fullname = subquery.newfullname from (select id,concat(firstname, ' ', lastname) as newfullname from users) as subquery where users.id = subquery.id", execution_options = None)

    print "Dropping firstname and lastname collumn"
    op.drop_column('users', 'firstname')
    op.drop_column('users', 'lastname')
    


def downgrade():
    
    connection = op.get_bind()
    
    op.drop_column('users', 'fullname')
