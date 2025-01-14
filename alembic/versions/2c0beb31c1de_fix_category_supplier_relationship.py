"""Fix Category-Supplier Relationship

Revision ID: 2c0beb31c1de
Revises: 51894d508514
Create Date: 2024-11-29 11:46:02.063673

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2c0beb31c1de'
down_revision: Union[str, None] = '51894d508514'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('categories_name_key', 'categories', type_='unique')
    op.drop_index('ix_categories_id', table_name='categories')
    op.drop_index('ix_products_id', table_name='products')
    op.drop_index('ix_products_name', table_name='products')
    op.add_column('suppliers', sa.Column('category_id', sa.Integer(), nullable=True))
    op.alter_column('suppliers', 'name',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    op.drop_index('ix_suppliers_id', table_name='suppliers')
    op.drop_constraint('suppliers_name_key', 'suppliers', type_='unique')
    op.create_foreign_key(None, 'suppliers', 'categories', ['category_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'suppliers', type_='foreignkey')
    op.create_unique_constraint('suppliers_name_key', 'suppliers', ['name'])
    op.create_index('ix_suppliers_id', 'suppliers', ['id'], unique=False)
    op.alter_column('suppliers', 'name',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.drop_column('suppliers', 'category_id')
    op.create_index('ix_products_name', 'products', ['name'], unique=True)
    op.create_index('ix_products_id', 'products', ['id'], unique=False)
    op.create_index('ix_categories_id', 'categories', ['id'], unique=False)
    op.create_unique_constraint('categories_name_key', 'categories', ['name'])
    # ### end Alembic commands ###
