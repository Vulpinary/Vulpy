"""Add password column to sellers table

Revision ID: ba5afb0576b5
Revises: 1d5ad5bf92bf
Create Date: 2024-11-29 13:15:07.943148

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ba5afb0576b5'
down_revision: Union[str, None] = '1d5ad5bf92bf'
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
