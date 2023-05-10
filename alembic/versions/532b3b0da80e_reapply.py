"""reapply

Revision ID: 532b3b0da80e
Revises: a8e9bd8632db
Create Date: 2023-05-11 02:45:22.827279

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '532b3b0da80e'
down_revision = 'a8e9bd8632db'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'user', 'occupation', ['occupation_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='foreignkey')
    # ### end Alembic commands ###
