"""Initial.

Revision ID: d32d0c142865
Revises: 
Create Date: 2023-05-13 22:51:07.782684

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "d32d0c142865"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade database."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "application",
        sa.Column("id", sa.String(length=32), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("version", sa.String(length=255), nullable=False),
        sa.Column("architect", sa.String(length=255), nullable=False),
        sa.Column("discarded", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
    )
    op.create_table(
        "server",
        sa.Column("id", sa.String(length=32), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("environment", sa.String(length=255), nullable=False),
        sa.Column("operating_system", sa.String(length=255), nullable=False),
        sa.Column("cpu", sa.String(length=255), nullable=False),
        sa.Column("ram", sa.String(length=255), nullable=False),
        sa.Column("hdd", sa.String(length=255), nullable=False),
        sa.Column("discarded", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
    )
    op.create_table(
        "credential",
        sa.Column("id", sa.String(length=32), nullable=False),
        sa.Column("server_id", sa.String(length=32), nullable=False),
        sa.Column("connection_type", sa.String(length=255), nullable=False),
        sa.Column("local_ip", sa.String(length=255), nullable=True),
        sa.Column("local_port", sa.String(length=255), nullable=True),
        sa.Column("public_ip", sa.String(length=255), nullable=True),
        sa.Column("public_port", sa.String(length=255), nullable=True),
        sa.Column("username", sa.String(length=255), nullable=False),
        sa.Column("password", sa.String(length=255), nullable=False),
        sa.Column("discarded", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["server_id"],
            ["server.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
    )
    op.create_table(
        "server_application",
        sa.Column("server_id", sa.String(length=32), nullable=False),
        sa.Column("application_id", sa.String(length=32), nullable=False),
        sa.Column("install_dir", sa.String(length=255), nullable=True),
        sa.Column("log_dir", sa.String(length=255), nullable=True),
        sa.ForeignKeyConstraint(
            ["application_id"],
            ["application.id"],
        ),
        sa.ForeignKeyConstraint(
            ["server_id"],
            ["server.id"],
        ),
        sa.PrimaryKeyConstraint("server_id", "application_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade database."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("server_application")
    op.drop_table("credential")
    op.drop_table("server")
    op.drop_table("application")
    # ### end Alembic commands ###
