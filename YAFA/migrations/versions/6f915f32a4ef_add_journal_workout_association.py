"""Add journal-workout association

Revision ID: 6f915f32a4ef
Revises: 022a1b00b7ae
Create Date: 2025-07-30 16:09:43.916568

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6f915f32a4ef'
down_revision = '022a1b00b7ae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('journal_workout_association',
    sa.Column('journal_id', sa.Integer(), nullable=False),
    sa.Column('workout_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['journal_id'], ['journal.id'], ),
    sa.ForeignKeyConstraint(['workout_id'], ['workout.id'], ),
    sa.PrimaryKeyConstraint('journal_id', 'workout_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('journal_workout_association')
    # ### end Alembic commands ###
