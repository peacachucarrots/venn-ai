"""initial schema

Revision ID: 31f00e4538fa
Revises: 
Create Date: 2025-07-19 16:13:54.071339

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '31f00e4538fa'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('surveys',
    sa.Column('survey_id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('survey_id')
    )
    op.create_table('visitors',
    sa.Column('visitor_id', sa.UUID(), nullable=False),
    sa.PrimaryKeyConstraint('visitor_id')
    )
    op.create_table('questions',
    sa.Column('question_id', sa.UUID(), nullable=False),
    sa.Column('survey_id', sa.UUID(), nullable=False),
    sa.Column('prompt', sa.String(), nullable=False),
    sa.Column('order_number', sa.Integer(), autoincrement=True, nullable=True),
    sa.ForeignKeyConstraint(['survey_id'], ['surveys.survey_id'], ),
    sa.PrimaryKeyConstraint('question_id')
    )
    op.create_table('responses',
    sa.Column('response_id', sa.UUID(), nullable=False),
    sa.Column('survey_id', sa.UUID(), nullable=False),
    sa.Column('visitor_id', sa.UUID(), nullable=False),
    sa.Column('body', sa.String(), nullable=True),
    sa.Column('submitted_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['survey_id'], ['surveys.survey_id'], ),
    sa.ForeignKeyConstraint(['visitor_id'], ['visitors.visitor_id'], ),
    sa.PrimaryKeyConstraint('response_id')
    )
    op.create_table('options',
    sa.Column('option_id', sa.UUID(), nullable=False),
    sa.Column('question_id', sa.UUID(), nullable=False),
    sa.Column('label', sa.String(), nullable=True),
    sa.Column('numeric_value', sa.Numeric(scale=2), nullable=True),
    sa.ForeignKeyConstraint(['question_id'], ['questions.question_id'], ),
    sa.PrimaryKeyConstraint('option_id')
    )
    op.create_table('answers',
    sa.Column('answer_id', sa.UUID(), nullable=False),
    sa.Column('option_id', sa.UUID(), nullable=True),
    sa.Column('response_id', sa.UUID(), nullable=False),
    sa.Column('free_text', sa.String(), nullable=False),
    sa.Column('numeric_value', sa.Numeric(scale=2), nullable=True),
    sa.ForeignKeyConstraint(['option_id'], ['options.option_id'], ),
    sa.ForeignKeyConstraint(['response_id'], ['responses.response_id'], ),
    sa.PrimaryKeyConstraint('answer_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('answers')
    op.drop_table('options')
    op.drop_table('responses')
    op.drop_table('questions')
    op.drop_table('visitors')
    op.drop_table('surveys')
    # ### end Alembic commands ###
