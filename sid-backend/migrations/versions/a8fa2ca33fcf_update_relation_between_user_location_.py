"""update relation between user & location table 2

Revision ID: a8fa2ca33fcf
Revises: b9a1ca867349
Create Date: 2023-09-12 11:11:20.616123

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'a8fa2ca33fcf'
down_revision: Union[str, None] = 'b9a1ca867349'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
