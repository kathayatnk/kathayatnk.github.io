"""empty message

Revision ID: ec75df459128
Revises: 4719b06f8a9f
Create Date: 2025-06-04 15:20:09.028913

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'ec75df459128'
down_revision: Union[str, None] = '4719b06f8a9f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('bank', 'created_time',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               comment='',
               existing_nullable=False)
    op.alter_column('bank', 'updated_time',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               comment='',
               existing_nullable=True)
    op.create_table_comment(
        'bank',
        '',
        existing_comment=None,
        schema=None
    )
    op.alter_column('card', 'created_time',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               comment='',
               existing_nullable=False)
    op.alter_column('card', 'updated_time',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               comment='',
               existing_nullable=True)
    op.create_table_comment(
        'card',
        '',
        existing_comment=None,
        schema=None
    )
    op.alter_column('device', 'created_time',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               comment='',
               existing_nullable=False)
    op.alter_column('device', 'updated_time',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               comment='',
               existing_nullable=True)
    op.create_table_comment(
        'device',
        '',
        existing_comment=None,
        schema=None
    )
    op.alter_column('user', 'salt',
               existing_type=postgresql.BYTEA(),
               comment='',
               existing_nullable=True)
    op.alter_column('user', 'created_time',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               comment='',
               existing_nullable=False)
    op.alter_column('user', 'updated_time',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               comment='',
               existing_nullable=True)
    op.create_table_comment(
        'user',
        '',
        existing_comment=None,
        schema=None
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table_comment(
        'user',
        existing_comment='',
        schema=None
    )
    op.alter_column('user', 'updated_time',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               comment=None,
               existing_comment='',
               existing_nullable=True)
    op.alter_column('user', 'created_time',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               comment=None,
               existing_comment='',
               existing_nullable=False)
    op.alter_column('user', 'salt',
               existing_type=postgresql.BYTEA(),
               comment=None,
               existing_comment='',
               existing_nullable=True)
    op.drop_table_comment(
        'device',
        existing_comment='',
        schema=None
    )
    op.alter_column('device', 'updated_time',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               comment=None,
               existing_comment='',
               existing_nullable=True)
    op.alter_column('device', 'created_time',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               comment=None,
               existing_comment='',
               existing_nullable=False)
    op.drop_table_comment(
        'card',
        existing_comment='',
        schema=None
    )
    op.alter_column('card', 'updated_time',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               comment=None,
               existing_comment='',
               existing_nullable=True)
    op.alter_column('card', 'created_time',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               comment=None,
               existing_comment='',
               existing_nullable=False)
    op.drop_table_comment(
        'bank',
        existing_comment='',
        schema=None
    )
    op.alter_column('bank', 'updated_time',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               comment=None,
               existing_comment='',
               existing_nullable=True)
    op.alter_column('bank', 'created_time',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               comment=None,
               existing_comment='',
               existing_nullable=False)
    # ### end Alembic commands ###
