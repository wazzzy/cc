"""claude-md CLI entry point."""

import argparse
from pathlib import Path

from templates.installer import init, list_templates


def cmd_list(args: argparse.Namespace) -> None:
    templates = list_templates()
    if not templates:
        print("  (none)")
        return
    max_name = max(len(name) for name, _ in templates)
    for name, default_path in templates:
        print(f"  {name:<{max_name}}    (default: ./{default_path}/)")


def cmd_init(args: argparse.Namespace) -> None:
    cwd = Path(args.cwd) if args.cwd else Path.cwd()
    try:
        status, dest = init(cwd, args.template, path=args.path, force=args.force)
    except ValueError as e:
        print(f"error: {e}")
        raise SystemExit(1)

    if status == "skipped":
        print(f"  skipped: {dest} already exists (use --force to overwrite)")
    else:
        print(f"  {status}: {dest}")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="claude-md",
        description="Copy CLAUDE.md templates into your project",
    )
    parser.add_argument(
        "--cwd",
        metavar="DIR",
        help="target project directory (default: current directory)",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="List available templates")
    list_parser.set_defaults(func=cmd_list)

    init_parser = subparsers.add_parser("init", help="Copy a CLAUDE.md template into your project")
    init_parser.add_argument("template", help="Template name (e.g. backend)")
    init_parser.add_argument("--path", metavar="DIR", help="Target directory (default: template's default)")
    init_parser.add_argument("--force", action="store_true", help="Overwrite existing CLAUDE.md")
    init_parser.set_defaults(func=cmd_init)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
