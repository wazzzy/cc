"""cc CLI entry point: unified skills + template commands."""

import argparse
from pathlib import Path

from skills.installer import install, list_skills, uninstall
from templates.installer import init, list_templates


# --- skills ---

def cmd_skills_install(args: argparse.Namespace) -> None:
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


def cmd_skills_uninstall(args: argparse.Namespace) -> None:
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


def cmd_skills_list(args: argparse.Namespace) -> None:
    skills = list_skills()
    if not skills:
        print("  (none)")
        return
    max_name = max(len(name) for name, _ in skills)
    for name, scope in skills:
        print(f"  {name:<{max_name}}    ({scope})")


# --- template ---

def cmd_template_init(args: argparse.Namespace) -> None:
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


def cmd_template_list(args: argparse.Namespace) -> None:
    templates = list_templates()
    if not templates:
        print("  (none)")
        return
    max_name = max(len(name) for name, _ in templates)
    for name, default_path in templates:
        print(f"  {name:<{max_name}}    (default: ./{default_path}/)")


# --- main ---

def main() -> None:
    parser = argparse.ArgumentParser(prog="cc", description="Claude Code tools")
    subparsers = parser.add_subparsers(dest="group", required=True)

    # skills
    skills_parser = subparsers.add_parser("skills", help="Manage Claude Code skills")
    skills_parser.add_argument("--cwd", metavar="DIR", help="target project directory")
    skills_sub = skills_parser.add_subparsers(dest="command", required=True)

    install_p = skills_sub.add_parser("install", help="Install skills (user-scoped by default)")
    install_p.add_argument("skills", nargs="*", metavar="SKILL")
    install_p.set_defaults(func=cmd_skills_install)

    uninstall_p = skills_sub.add_parser("uninstall", help="Uninstall skills")
    uninstall_p.add_argument("skills", nargs="*", metavar="SKILL")
    uninstall_p.set_defaults(func=cmd_skills_uninstall)

    list_p = skills_sub.add_parser("list", help="List available skills")
    list_p.set_defaults(func=cmd_skills_list)

    # template
    template_parser = subparsers.add_parser("template", help="Manage CLAUDE.md templates")
    template_parser.add_argument("--cwd", metavar="DIR", help="target project directory")
    template_sub = template_parser.add_subparsers(dest="command", required=True)

    init_p = template_sub.add_parser("init", help="Copy a CLAUDE.md template into your project")
    init_p.add_argument("template", help="Template name (e.g. django)")
    init_p.add_argument("--path", metavar="DIR", help="Target directory (overrides template default)")
    init_p.add_argument("--force", action="store_true", help="Overwrite existing CLAUDE.md")
    init_p.set_defaults(func=cmd_template_init)

    tlist_p = template_sub.add_parser("list", help="List available templates")
    tlist_p.set_defaults(func=cmd_template_list)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
