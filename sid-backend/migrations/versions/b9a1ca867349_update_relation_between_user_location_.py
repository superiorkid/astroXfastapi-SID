"""update relation between user & location table

Revision ID: b9a1ca867349
Revises: 344525e82ce9
Create Date: 2023-09-12 10:44:10.264732

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'b9a1ca867349'
down_revision: Union[str, None] = '344525e82ce9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('article', sa.Column('user_id', sa.Integer(), nullable=True))
    op.drop_constraint('article_author_id_fkey', 'article', type_='foreignkey')
    op.create_foreign_key(None, 'article', 'user', ['user_id'], ['id'])
    op.drop_column('article', 'author_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('article', sa.Column('author_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'article', type_='foreignkey')
    op.create_foreign_key('article_author_id_fkey', 'article', 'user', ['author_id'], ['id'])
    op.drop_column('article', 'user_id')
    # ### end Alembic commands ###
