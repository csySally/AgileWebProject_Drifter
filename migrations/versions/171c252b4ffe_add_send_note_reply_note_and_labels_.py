"""add send_note, reply_note and labels table

Revision ID: 171c252b4ffe
Revises: 1d523e191313
Create Date: 2024-05-02 22:46:44.477484

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '171c252b4ffe'
down_revision = '1d523e191313'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('labels',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('label', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reply__note',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(length=140), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('anonymous', sa.Boolean(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('reply__note', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_reply__note_timestamp'), ['timestamp'], unique=False)

    with op.batch_alter_table('send__note', schema=None) as batch_op:
        batch_op.add_column(sa.Column('labels_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('anonymous', sa.Boolean(), nullable=True))
        batch_op.create_foreign_key(None, 'labels', ['labels_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('send__note', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('anonymous')
        batch_op.drop_column('labels_id')

    with op.batch_alter_table('reply__note', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_reply__note_timestamp'))

    op.drop_table('reply__note')
    op.drop_table('labels')
    # ### end Alembic commands ###
