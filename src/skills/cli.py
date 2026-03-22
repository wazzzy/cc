"""skills CLI entry point."""

import argparse
from pathlib import Path

from skills.installer import install, list_skills, uninstall


def cmd_install(args: argparse.Namespace) -> None:
    cwd = Path(args.cwd) if args.cwd else Path.cwd()
    names = args.skills or None
    try:
        skills = install(cwd, names)
    except ValueError as e:
        print(f"error: {e}")
        raise SystemExit(1)
    for name in skills:
        print(f"  installed: {name}")
    print(f"\n{len(skills)} skill(s) installed to {cwd / '.claude' / 'skills'}")


def cmd_uninstall(args: argparse.Namespace) -> None:
    cwd = Path(args.cwd) if args.cwd else Path.cwd()
    names = args.skills or None
    try:
        results = uninstall(cwd, names)
    except ValueError as e:
        print(f"error: {e}")
        raise SystemExit(1)
    for name, status in results.items():
        print(f"  {status}: {name}")
    removed = sum(1 for s in results.values() if s == "removed")
    skipped = sum(1 for s in results.values() if s == "skipped")
    print(f"\n{removed} skill(s) removed, {skipped} skipped")


def cmd_list(args: argparse.Namespace) -> None:
    for name in list_skills():
        print(f"  {name}")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="skills",
        description="Install Claude Code skills into your project",
    )
    parser.add_argument(
        "--cwd",
        metavar="DIR",
        help="target project directory (default: current directory)",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    install_parser = subparsers.add_parser("install", help="Install skills (all if none specified)")
    install_parser.add_argument("skills", nargs="*", metavar="SKILL")
    install_parser.set_defaults(func=cmd_install)

    uninstall_parser = subparsers.add_parser("uninstall", help="Uninstall skills (all if none specified)")
    uninstall_parser.add_argument("skills", nargs="*", metavar="SKILL")
    uninstall_parser.set_defaults(func=cmd_uninstall)

    list_parser = subparsers.add_parser("list", help="List available skills")
    list_parser.set_defaults(func=cmd_list)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
