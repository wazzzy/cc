"""skills CLI: install, uninstall, list Claude Code skills."""

import argparse
from pathlib import Path

from skills.installer import install, list_skills, uninstall


def cmd_install(args: argparse.Namespace) -> None:
    cwd = Path(args.cwd) if args.cwd else Path.cwd()
    names = args.skills or None
    if args.cwd and names is None:
        print("warning: --cwd has no effect on user-level skills")
    try:
        results = install(cwd, names)
    except ValueError as e:
        print(f"error: {e}")
        raise SystemExit(1)
    for name, scope, dest in results:
        print(f"  installed: {name} ({scope}) -> {dest}")
    print(f"\n{len(results)} skill(s) installed")


def cmd_uninstall(args: argparse.Namespace) -> None:
    cwd = Path(args.cwd) if args.cwd else Path.cwd()
    names = args.skills or None
    if args.cwd and names is None:
        print("warning: --cwd has no effect on user-level skills")
    try:
        results = uninstall(cwd, names)
    except ValueError as e:
        print(f"error: {e}")
        raise SystemExit(1)
    for name, (status, scope) in results.items():
        print(f"  {status}: {name} ({scope})")
    removed = sum(1 for s, _ in results.values() if s == "removed")
    skipped = sum(1 for s, _ in results.values() if s == "skipped")
    print(f"\n{removed} removed, {skipped} skipped")


def cmd_list(args: argparse.Namespace) -> None:
    skills = list_skills()
    if not skills:
        print("  (none)")
        return
    max_name = max(len(name) for name, _ in skills)
    for name, scope in skills:
        print(f"  {name:<{max_name}}    ({scope})")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="skills",
        description="Install Claude Code skills into your project",
    )
    parser.add_argument("--cwd", metavar="DIR", help="target project directory (default: cwd)")
    subparsers = parser.add_subparsers(dest="command", required=True)

    install_p = subparsers.add_parser("install", help="Install skills (user-scoped by default)")
    install_p.add_argument("skills", nargs="*", metavar="SKILL")
    install_p.set_defaults(func=cmd_install)

    uninstall_p = subparsers.add_parser("uninstall", help="Uninstall skills")
    uninstall_p.add_argument("skills", nargs="*", metavar="SKILL")
    uninstall_p.set_defaults(func=cmd_uninstall)

    list_p = subparsers.add_parser("list", help="List available skills")
    list_p.set_defaults(func=cmd_list)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
