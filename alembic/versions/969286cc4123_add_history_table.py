"""add history table

Revision ID: 969286cc4123
Revises: db8aba970509
Create Date: 2023-05-15 10:57:36.570422

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "969286cc4123"
down_revision = "db8aba970509"
branch_labels = None
depends_on = None

sql_create_text = """
CREATE OR REPLACE FUNCTION user_update_history() RETURNS trigger AS
$BODY$
BEGIN
    IF TG_OP = 'UPDATE' THEN
        INSERT INTO history(old, new)
        VALUES (row_to_json(old)::jsonb, row_to_json(new)::jsonb);
    END IF;
    RETURN NEW;
END;
$BODY$
LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER user_update_history
    AFTER UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION user_update_history();
"""

sql_drop_text = """
DROP TRIGGER user_update_history;
DROP FUNCTION user_update_history;
"""


def upgrade() -> None:
    op.create_table(
        "history",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column(
            "old", postgresql.JSONB(astext_type=sa.Text()), nullable=True
        ),
        sa.Column(
            "new", postgresql.JSONB(astext_type=sa.Text()), nullable=True
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.execute(sqltext=sql_create_text)


def downgrade() -> None:
    op.drop_table("history")
    op.execute(sql_drop_text)
