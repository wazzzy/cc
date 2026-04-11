"""templates CLI: copy CLAUDE.md templates into projects."""

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
    target = "pi" if args.pi else "claude"
    try:
        status, dest = init(cwd, args.name, path=args.path, force=args.force, target=target)
    except ValueError as e:
        print(f"error: {e}")
        raise SystemExit(1)
    if status == "skipped":
        print(f"  skipped: {dest} already exists (use --force to overwrite)")
    else:
        print(f"  {status}: {dest}")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="templates",
        description="Copy CLAUDE.md templates into your project",
    )
    parser.add_argument("--cwd", metavar="DIR", help="target project directory (default: cwd)")
    subparsers = parser.add_subparsers(dest="name", required=True)

    list_p = subparsers.add_parser("list", help="List available templates")
    list_p.set_defaults(func=cmd_list)

    # Register each known template as a subcommand dynamically
    for tpl_name, default_path in list_templates():
        tpl_p = subparsers.add_parser(tpl_name, help=f"Copy {tpl_name} CLAUDE.md (default: ./{default_path}/)")
        tpl_p.add_argument("--path", metavar="DIR", help="Target directory (overrides default)")
        tpl_p.add_argument("--force", action="store_true", help="Overwrite existing CLAUDE.md")
        tpl_p.add_argument("--pi", action="store_true", help="Target pi agent (accepted for consistency; path is unchanged)")
        tpl_p.set_defaults(func=cmd_init, name=tpl_name)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
