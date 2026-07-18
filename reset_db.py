"""Dev convenience: wipe the database and rebuild it from the Alembic
migrations, so schema state always matches what migrations would produce
(rather than bypassing them via Base.metadata, which could drift)."""

from alembic import command
from alembic.config import Config

print("Downgrading to base (dropping all tables)...")
alembic_cfg = Config("alembic.ini")
command.downgrade(alembic_cfg, "base")

print("Upgrading to head (recreating all tables)...")
command.upgrade(alembic_cfg, "head")

print("Database reset successfully via Alembic migrations!")
