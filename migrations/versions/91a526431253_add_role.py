"""Add Role

Revision ID: 91a526431253
Revises: dbe5d351143a
Create Date: 2025-04-16 18:22:05.907148

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "91a526431253"
down_revision: Union[str, None] = "dbe5d351143a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


role_enum = postgresql.ENUM("ADMIN", "USER", name="role")


def upgrade() -> None:
    # Step 2: Create the ENUM in PostgreSQL
    role_enum.create(op.get_bind(), checkfirst=True)

    # Step 3: Add the column using the now-existing ENUM
    op.add_column(
        "users", sa.Column("role", role_enum, nullable=False, server_default="USER")
    )


def downgrade() -> None:
    # Step 4: Drop the column
    op.drop_column("users", "role")

    # Step 5: Drop the ENUM type
    role_enum.drop(op.get_bind(), checkfirst=True)
