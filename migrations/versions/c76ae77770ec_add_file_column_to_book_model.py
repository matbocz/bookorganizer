"""Add file column to Book model

Revision ID: c76ae77770ec
Revises: 707efa5d4061
Create Date: 2021-10-10 10:31:50.584807

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c76ae77770ec'
down_revision = '707efa5d4061'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('books', sa.Column('file', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('books', 'file')
    # ### end Alembic commands ###
