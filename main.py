#!/usr/bin/env python3
"""CLI entry point for the Password Strength Checker and Policy Analyzer.

Usage:
    python main.py                        # Interactive mode
    python main.py "MyP@ssw0rd"           # Check a specific password
    python main.py --breach "password"    # Include HIBP breach check
    python main.py --batch passwords.txt  # Check a file of passwords
"""

from __future__ import annotations

import argparse
import getpass
import sys

from password_checker.display import print_result
from password_checker.policy import PasswordPolicy
from password_checker.scoring import score_password


def build_parser() -> argparse.ArgumentParser:
    """Build and return the argument parser."""
    parser = argparse.ArgumentParser(
        prog="password-strength-checker",
        description="🔐 Password Strength Checker and Policy Analyzer",
        epilog="Examples:\n"
        "  python main.py\n"
        "  python main.py 'MyP@ssw0rd!123'\n"
        "  python main.py --breach --min-length 16 'Test1234!'\n"
        "  python main.py --batch passwords.txt\n",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "password",
        nargs="?",
        default=None,
        help="Password to check (omit for interactive/hidden prompt).",
    )

    parser.add_argument(
        "--breach",
        action="store_true",
        default=False,
        help="Check password against the Have I Been Pwned breach database.",
    )

    parser.add_argument(
        "--batch",
        metavar="FILE",
        default=None,
        help="Check every password in FILE (one per line).",
    )

    # ── Policy overrides ──────────────────────────────────────────────────
    policy_group = parser.add_argument_group("Policy overrides")
    policy_group.add_argument(
        "--min-length",
        type=int,
        default=12,
        help="Minimum password length (default: 12).",
    )
    policy_group.add_argument(
        "--max-length",
        type=int,
        default=128,
        help="Maximum password length (default: 128).",
    )
    policy_group.add_argument(
        "--no-require-upper",
        action="store_true",
        help="Do not require uppercase letters.",
    )
    policy_group.add_argument(
        "--no-require-lower",
        action="store_true",
        help="Do not require lowercase letters.",
    )
    policy_group.add_argument(
        "--no-require-digit",
        action="store_true",
        help="Do not require digits.",
    )
    policy_group.add_argument(
        "--no-require-special",
        action="store_true",
        help="Do not require special characters.",
    )

    return parser


def policy_from_args(args: argparse.Namespace) -> PasswordPolicy:
    """Build a PasswordPolicy from parsed CLI arguments."""
    return PasswordPolicy(
        min_length=args.min_length,
        max_length=args.max_length,
        require_uppercase=not args.no_require_upper,
        require_lowercase=not args.no_require_lower,
        require_digit=not args.no_require_digit,
        require_special=not args.no_require_special,
    )


def check_one(password: str, policy: PasswordPolicy, check_breach: bool) -> None:
    """Score and display results for a single password."""
    result = score_password(password, policy=policy, check_breach=check_breach)
    print_result(result)


def main(argv: list[str] | None = None) -> None:
    """Run the CLI."""
    parser = build_parser()
    args = parser.parse_args(argv)
    policy = policy_from_args(args)

    # ── Batch mode ────────────────────────────────────────────────────────
    if args.batch:
        try:
            with open(args.batch, "r", encoding="utf-8") as f:
                passwords = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"Error: File '{args.batch}' not found.", file=sys.stderr)
            sys.exit(1)

        print(f"\n🔐 Checking {len(passwords)} password(s) from '{args.batch}'...\n")
        for pw in passwords:
            check_one(pw, policy, args.breach)
        return

    # ── Single password ───────────────────────────────────────────────────
    if args.password:
        check_one(args.password, policy, args.breach)
        return

    # ── Interactive mode ──────────────────────────────────────────────────
    print("\n🔐 Password Strength Checker and Policy Analyzer")
    print("=" * 50)
    print("Type 'quit' or 'exit' to stop.\n")

    while True:
        try:
            password = getpass.getpass("Enter a password to check (hidden): ")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye! 👋")
            break

        if password.lower() in ("quit", "exit", "q"):
            print("Goodbye! 👋")
            break

        if not password:
            print("Please enter a non-empty password.\n")
            continue

        check_one(password, policy, args.breach)


if __name__ == "__main__":
    main()
