"""Torna campos antigos do curso opcionais

Revision ID: 7d4a8d3cfa5d
Revises: 44f78ee3dd6d
Create Date: 2026-11-24 23:42:58.933177

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7d4a8d3cfa5d'
down_revision = '44f78ee3dd6d'
branch_labels = None
depends_on = None


def upgrade():
    # Altera somente a tabela de cursos.
    with op.batch_alter_table('cursos', schema=None) as batch_op:
        batch_op.alter_column(
            'codigo',
            existing_type=sa.VARCHAR(length=30),
            nullable=True
        )
        batch_op.alter_column(
            'carga_horaria',
            existing_type=sa.INTEGER(),
            nullable=True
        )


def downgrade():
    # Retorna as colunas de cursos à obrigatoriedade anterior.
    with op.batch_alter_table('cursos', schema=None) as batch_op:
        batch_op.alter_column(
            'carga_horaria',
            existing_type=sa.INTEGER(),
            nullable=False
        )
        batch_op.alter_column(
            'codigo',
            existing_type=sa.VARCHAR(length=30),
            nullable=False
        )
