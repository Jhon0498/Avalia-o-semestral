"""Adiciona tabela de cursos

Revision ID: 44f78ee3dd6d
Revises: e0c112c17fef
"""

from alembic import op
import sqlalchemy as sa

# Identificadores da migração.
revision = '44f78ee3dd6d'
down_revision = 'e0c112c17fef'
branch_labels = None
depends_on = None


# Cria somente a tabela de cursos.
def upgrade():
    op.create_table(
        'cursos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(length=120), nullable=False),
        sa.Column('codigo', sa.String(length=30), nullable=False),
        sa.Column('carga_horaria', sa.Integer(), nullable=False),
        sa.Column('descricao', sa.Text(), nullable=True),
        sa.Column('data_cadastro', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('codigo')
    )


# Remove somente a tabela de cursos em caso de reversão.
def downgrade():
    op.drop_table('cursos')
