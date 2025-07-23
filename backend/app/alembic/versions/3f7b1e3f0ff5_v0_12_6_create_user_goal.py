"""v0.12.6 create user goal

Revision ID: 3f7b1e3f0ff5
Revises: 72e2079576d3
Create Date: 2025-07-04 20:58:25.804685

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3f7b1e3f0ff5'
down_revision: Union[str, None] = '72e2079576d3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table(
        "users_goals",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.PrimaryKeyConstraint("id"),
        
        sa.Column(
            "user_id",
            sa.Integer(),
            nullable=False,
            comment="User ID that the goals belongs",
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),

        sa.Column('activity_type', sa.Integer(), nullable=False, comment='Activity type'),

        sa.Column(
            "interval",
            sa.String(length=250),
            nullable=False,
            comment="Goal interval (e.g., 'daily', 'weekly', 'monthly')",
        ),

        sa.Column(
            "goal_duration",
            sa.Integer(),
            nullable=False,
            comment="Goal duration in hours (e.g., 10 for 10 hours)",
        ),

        sa.Column(
            "goal_distance",
            sa.Integer(),
            nullable=False,
            comment="Goal distance in meters (e.g., 10000 for 10 km)",
        ),

        sa.Column(
            "goal_elevation",
            sa.Integer(),
            nullable=False,
            comment="Goal elevation in meters (e.g., 1000 for 1000 m)",
        ),

        sa.Column(
            "goal_calories",
            sa.Integer(),
            nullable=False,
            comment="Goal calories in kcal (e.g., 5000 for 5000 kcal)",
        ),

        sa.Column(
            "goal_steps",
            sa.Integer(),
            nullable=False,
            comment="Goal steps (e.g., 10000 for 10,000 steps)",
        ),

        sa.Column(
            "goal_count",
            sa.Integer(),
            nullable=False,
            comment="Goal count (e.g., 5 for 5 activities)",
        ),
    )
    op.create_index(
        op.f("ix_users_goals_user_id"),
        "users_goals",
        ["user_id"],
        unique=False,
    )

def downgrade() -> None:
    op.drop_index(op.f("ix_users_goals_user_id"), table_name="users_goals")
    op.drop_table("users_goals")
