"""Add phone_number column

Revision ID: 9a5c7bbb057a
Revises: a02e99a1cde4
Create Date: 2024-07-09 16:26:59.244355

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9a5c7bbb057a'
down_revision: Union[str, None] = 'a02e99a1cde4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True ))


def downgrade() -> None:
    pass
