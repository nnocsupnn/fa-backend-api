"""Drop col in user

Revision ID: e00f0c17b2ee
Revises: 04cf911f29db
Create Date: 2023-05-24 00:58:14.665955

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'e00f0c17b2ee'
down_revision = '04cf911f29db'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_user_testCol', table_name='user')
    op.drop_column('user', 'testCol')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('testCol', mysql.VARCHAR(length=50), nullable=True))
    op.create_index('ix_user_testCol', 'user', ['testCol'], unique=False)
    # ### end Alembic commands ###