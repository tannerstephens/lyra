"""empty message

Revision ID: e4902ce88cc8
Revises: 373480932842
Create Date: 2021-01-28 14:19:23.769401

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e4902ce88cc8'
down_revision = '373480932842'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('plugin', sa.Column('disabled', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('plugin', 'disabled')
    # ### end Alembic commands ###