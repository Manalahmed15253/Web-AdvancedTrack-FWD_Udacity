"""empty message

Revision ID: a6801d6c0cf0
Revises: 2f316bce6902
Create Date: 2020-10-22 01:18:52.051542

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a6801d6c0cf0'
down_revision = '2f316bce6902'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('shows',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('artist_id', sa.Integer(), nullable=True),
    sa.Column('venue_id', sa.Integer(), nullable=True),
    sa.Column('start_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['artist_id'], ['artist.id'], ),
    sa.ForeignKeyConstraint(['venue_id'], ['venue.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('Shows')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Shows',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"Shows_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('artist_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('venue_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('start_time', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['artist_id'], ['artist.id'], name='Shows_artist_id_fkey'),
    sa.ForeignKeyConstraint(['venue_id'], ['venue.id'], name='Shows_venue_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='Shows_pkey')
    )
    op.drop_table('shows')
    # ### end Alembic commands ###
