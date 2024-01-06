"""Initial.

Revision ID: 6b54f29e524e
Revises: 
Create Date: 2024-01-06 03:19:21.845305

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6b54f29e524e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('application',
    sa.Column('id', sa.String(length=32), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('version', sa.String(length=255), nullable=True),
    sa.Column('architect', sa.String(length=255), nullable=True),
    sa.Column('discarded', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('server',
    sa.Column('id', sa.String(length=32), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('cpu', sa.String(length=255), nullable=True),
    sa.Column('ram', sa.String(length=255), nullable=True),
    sa.Column('hdd', sa.String(length=255), nullable=True),
    sa.Column('environment', sa.String(length=255), nullable=True),
    sa.Column('operating_system', sa.JSON(), nullable=True),
    sa.Column('status', sa.String(length=255), nullable=True),
    sa.Column('discarded', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('credential',
    sa.Column('id', sa.String(length=32), nullable=False),
    sa.Column('server_id', sa.String(length=32), nullable=True),
    sa.Column('connection_type', sa.String(length=255), nullable=True),
    sa.Column('local_ip', sa.String(length=255), nullable=True),
    sa.Column('local_port', sa.String(length=255), nullable=True),
    sa.Column('public_ip', sa.String(length=255), nullable=True),
    sa.Column('public_port', sa.String(length=255), nullable=True),
    sa.Column('username', sa.String(length=255), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.Column('discarded', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['server_id'], ['server.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('server_application',
    sa.Column('server_id', sa.String(length=32), nullable=False),
    sa.Column('application_id', sa.String(length=32), nullable=False),
    sa.Column('install_dir', sa.String(length=255), nullable=True),
    sa.Column('log_dir', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['application_id'], ['application.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['server_id'], ['server.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('server_id', 'application_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('server_application')
    op.drop_table('credential')
    op.drop_table('server')
    op.drop_table('application')
    # ### end Alembic commands ###