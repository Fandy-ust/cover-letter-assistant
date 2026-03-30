#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import shutil


ROOT = Path.cwd()
ACTIVE_DIR = ROOT / "active_application"
APPLICATIONS_DIR = ROOT / "applications"
RAW_JOB_DIR = ROOT / "raw_inputs" / "job"
ACTIVE_MARKER = ACTIVE_DIR / ".active"


def copy_tree_contents(src: Path, dst: Path) -> None:
    dst.mkdir(parents=True, exist_ok=True)
    for path in src.iterdir():
        target = dst / path.name
        if path.is_dir():
            if target.exists():
                shutil.rmtree(target)
            shutil.copytree(path, target)
        else:
            shutil.copy2(path, target)


def current_slug() -> str:
    if not ACTIVE_MARKER.exists():
        return "none"
    return ACTIVE_MARKER.read_text(encoding="utf-8").strip() or "none"


def save_current() -> None:
    slug = current_slug()
    if slug == "none":
        print("No active application to save.")
        return

    destination = APPLICATIONS_DIR / slug
    destination.mkdir(parents=True, exist_ok=True)
    copy_tree_contents(ACTIVE_DIR, destination)
    print(f"Saved active application to {destination}")


def clear_job_inputs() -> None:
    RAW_JOB_DIR.mkdir(parents=True, exist_ok=True)
    for path in list(RAW_JOB_DIR.iterdir()):
        if path.name == "README.md":
            continue
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()
    print(f"Cleared job inputs in {RAW_JOB_DIR}")


def reset_active() -> None:
    ACTIVE_DIR.mkdir(parents=True, exist_ok=True)
    submission_dir = ACTIVE_DIR / "submission"

    for path in list(ACTIVE_DIR.iterdir()):
        if path.name == "README.md":
            continue
        if path.name == "submission" and path.is_dir():
            submission_dir.mkdir(parents=True, exist_ok=True)
            for subpath in list(path.iterdir()):
                if subpath.name == "README.md":
                    continue
                if subpath.is_dir():
                    shutil.rmtree(subpath)
                else:
                    subpath.unlink()
            continue
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()

    submission_dir.mkdir(parents=True, exist_ok=True)
    print(f"Reset active workspace in {ACTIVE_DIR}")


def load_target(slug: str) -> None:
    source = APPLICATIONS_DIR / slug
    if not source.exists():
        raise FileNotFoundError(f"Saved application not found: {source}")

    copy_tree_contents(source, ACTIVE_DIR)
    ACTIVE_MARKER.write_text(f"{slug}\n", encoding="utf-8")
    print(f"Loaded application {slug} into {ACTIVE_DIR}")


def init_new(slug: str) -> None:
    for rel in ["job_description.md", "application_brief.md", "final_draft.md"]:
        (ACTIVE_DIR / rel).write_text("", encoding="utf-8")
    (ACTIVE_DIR / "submission").mkdir(parents=True, exist_ok=True)
    ACTIVE_MARKER.write_text(f"{slug}\n", encoding="utf-8")
    print(f"Initialized new active application {slug}")


def switch_to(slug: str) -> None:
    save_current()
    clear_job_inputs()
    reset_active()
    load_target(slug)
    print(
        f"Switched to {slug}. active_application/ is ready, and raw_inputs/job/ has been cleared."
    )


def create_new(slug: str) -> None:
    save_current()
    clear_job_inputs()
    reset_active()
    init_new(slug)
    print(f"New application {slug} is active. Run job-researcher to begin.")


def list_applications() -> None:
    slug = current_slug()
    print(f"Current active: {slug}")
    if not APPLICATIONS_DIR.exists():
        return
    for path in sorted(p for p in APPLICATIONS_DIR.iterdir() if p.is_dir()):
        print(path.name)


def delete_application(slug: str, confirm: bool) -> None:
    if not confirm:
        raise ValueError("Refusing to delete without --confirm")

    target = APPLICATIONS_DIR / slug
    if not target.exists():
        raise FileNotFoundError(f"Saved application not found: {target}")
    if not target.is_dir():
        raise NotADirectoryError(f"Not an application directory: {target}")

    shutil.rmtree(target)
    print(f"Deleted saved application {slug}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage the cover letter active workspace.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("save-current")
    subparsers.add_parser("clear-job-inputs")
    subparsers.add_parser("reset-active")
    load_parser = subparsers.add_parser("load")
    load_parser.add_argument("slug")
    init_parser = subparsers.add_parser("init-new")
    init_parser.add_argument("slug")
    switch_parser = subparsers.add_parser("switch")
    switch_parser.add_argument("slug")
    new_parser = subparsers.add_parser("new")
    new_parser.add_argument("slug")
    subparsers.add_parser("list")
    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument("slug")
    delete_parser.add_argument("--confirm", action="store_true")

    return parser


def main() -> int:
    args = build_parser().parse_args()

    if args.command == "save-current":
        save_current()
    elif args.command == "clear-job-inputs":
        clear_job_inputs()
    elif args.command == "reset-active":
        reset_active()
    elif args.command == "load":
        load_target(args.slug)
    elif args.command == "init-new":
        init_new(args.slug)
    elif args.command == "switch":
        switch_to(args.slug)
    elif args.command == "new":
        create_new(args.slug)
    elif args.command == "list":
        list_applications()
    elif args.command == "delete":
        delete_application(args.slug, args.confirm)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
