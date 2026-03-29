#!/usr/bin/env python3
# Copyright (c) 2026 Diego Silva Morais <lukewaresoftwarehouse@gmail.com>

"""
Setup script to configure agent access permissions.

Usage:
    python scripts/setup_agent_permissions.py grant-access \
        --agent-slug clawdevsai/searxng-runtime \
        --username po

    python scripts/setup_agent_permissions.py list-permissions \
        --agent-slug clawdevsai/searxng-runtime

    python scripts/setup_agent_permissions.py revoke-access \
        --agent-slug clawdevsai/searxng-runtime \
        --username po
"""

import asyncio
import argparse
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import AsyncSessionLocal
from app.models import AgentPermission, User


async def grant_access(agent_slug: str, username: str) -> None:
    """Grant access to an agent for a user."""
    async with AsyncSessionLocal() as session:
        # Find user
        result = await session.exec(select(User).where(User.username == username))
        user = result.first()
        if not user:
            print(f"❌ User '{username}' not found")
            return

        # Check if permission already exists
        result = await session.exec(
            select(AgentPermission).where(
                (AgentPermission.agent_slug == agent_slug)
                & (AgentPermission.user_id == user.id)
            )
        )
        existing = result.first()
        if existing:
            print(f"⚠️  Permission already exists for {username} -> {agent_slug}")
            return

        # Create permission
        permission = AgentPermission(
            agent_slug=agent_slug,
            user_id=user.id,
        )
        session.add(permission)
        await session.commit()
        print(f"✅ Granted access: {username} -> {agent_slug}")


async def revoke_access(agent_slug: str, username: str) -> None:
    """Revoke access to an agent for a user."""
    async with AsyncSessionLocal() as session:
        # Find user
        result = await session.exec(select(User).where(User.username == username))
        user = result.first()
        if not user:
            print(f"❌ User '{username}' not found")
            return

        # Find and delete permission
        result = await session.exec(
            select(AgentPermission).where(
                (AgentPermission.agent_slug == agent_slug)
                & (AgentPermission.user_id == user.id)
            )
        )
        permission = result.first()
        if not permission:
            print(f"❌ Permission not found for {username} -> {agent_slug}")
            return

        await session.delete(permission)
        await session.commit()
        print(f"✅ Revoked access: {username} -> {agent_slug}")


async def list_permissions(agent_slug: str) -> None:
    """List all users with access to an agent."""
    async with AsyncSessionLocal() as session:
        result = await session.exec(
            select(AgentPermission, User).where(
                (AgentPermission.agent_slug == agent_slug)
                & (AgentPermission.user_id == User.id)
            )
        )
        rows = result.all()

        if not rows:
            print(f"No permissions configured for '{agent_slug}'")
            print("(All users have access)")
            return

        print(f"\nUsers with access to '{agent_slug}':")
        for permission, user in rows:
            print(f"  • {user.username} ({user.role})")


async def main():
    parser = argparse.ArgumentParser(
        description="Setup agent access permissions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Grant command
    grant_parser = subparsers.add_parser("grant-access", help="Grant access to an agent")
    grant_parser.add_argument("--agent-slug", required=True, help="Agent slug (e.g., clawdevsai/searxng-runtime)")
    grant_parser.add_argument("--username", required=True, help="Username to grant access")

    # Revoke command
    revoke_parser = subparsers.add_parser("revoke-access", help="Revoke access to an agent")
    revoke_parser.add_argument("--agent-slug", required=True, help="Agent slug")
    revoke_parser.add_argument("--username", required=True, help="Username to revoke access")

    # List command
    list_parser = subparsers.add_parser("list-permissions", help="List permissions for an agent")
    list_parser.add_argument("--agent-slug", required=True, help="Agent slug")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    if args.command == "grant-access":
        await grant_access(args.agent_slug, args.username)
    elif args.command == "revoke-access":
        await revoke_access(args.agent_slug, args.username)
    elif args.command == "list-permissions":
        await list_permissions(args.agent_slug)


if __name__ == "__main__":
    asyncio.run(main())
