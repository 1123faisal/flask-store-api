"""increase password column length to 255

Revision ID: 92a36e8fafd0
Revises: 5bc4d2709813
Create Date: 2026-09-19 00:31:25.858059

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '92a36e8fafd0'
down_revision = '5bc4d2709813'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=sa.VARCHAR(length=80),
               type_=sa.String(length=255),
               existing_nullable=False)


def downgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=sa.String(length=255),
               type_=sa.VARCHAR(length=80),
               existing_nullable=False)
