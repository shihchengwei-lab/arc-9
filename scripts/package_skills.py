"""Build the standalone skill from its approved source."""

import argparse
import io
import json
import os
import stat
import zipfile
from pathlib import Path
from uuid import uuid4


SKILL_NAME = "arc9"
REFERENCE_NAMES = ("review.md", "output.md")
DESCRIPTION = "使用者呼叫 arc9 濾鏡時，以唯讀方式依任務材料審查方案、說明未知並提出必要改動建議。"


def validate_output_name(path):
    if os.name == "nt" and path.name != ".." and path.name.rstrip(" .") != path.name:
        raise ValueError(f"Package output contains an ambiguous Windows name: {path}")


def output_mode(path):
    validate_output_name(path)
    try:
        entry = path.lstat()
    except FileNotFoundError:
        return None
    if stat.S_ISLNK(entry.st_mode) or (
        getattr(entry, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT
    ):
        raise ValueError(f"Package output contains a linked path: {path}")
    return entry.st_mode


def output_directory_exists(path):
    mode = output_mode(path)
    if mode is None:
        return False
    if not stat.S_ISDIR(mode):
        raise ValueError(f"Package output requires a directory: {path}")
    return True


def existing_outputs(output, skills_output, archive_output):
    for directory in reversed(output.parents):
        output_directory_exists(directory)

    files, directories = [], []
    if not output_directory_exists(output):
        return files, directories

    managed_paths = (skills_output, archive_output)
    names = {path.name for path in output.iterdir()}
    if os.name == "nt":
        managed_names = {path.name.casefold() for path in managed_paths}
        for name in names:
            if name.rstrip(" .").casefold() in managed_names:
                validate_output_name(output / name)
    for path in managed_paths:
        if path.name not in names and output_mode(path) is not None:
            raise ValueError(f"Package output name differs from expected: {path}")

    pending = [skills_output] if output_directory_exists(skills_output) else []
    while pending:
        for path in pending.pop().iterdir():
            mode = output_mode(path)
            if mode is None:
                raise ValueError(f"Package output changed during inspection: {path}")
            if stat.S_ISDIR(mode):
                directories.append(path)
                pending.append(path)
            elif stat.S_ISREG(mode):
                files.append(path)
            else:
                raise ValueError(f"Package output requires a regular file or directory: {path}")

    mode = output_mode(archive_output)
    if mode is not None:
        if not stat.S_ISREG(mode):
            raise ValueError(f"Package archive requires a regular file: {archive_output}")
        files.append(archive_output)
    return files, directories


def replace_output_file(path, content):
    temporary = path.with_name(f".{path.name}.{uuid4().hex}.tmp")
    stream = temporary.open("xb")
    try:
        with stream:
            stream.write(content)
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def package(root, output, check=False):
    root, output = Path(root), Path(output).absolute()
    approved = (root / f"drafts/{SKILL_NAME}.md").read_text(encoding="utf-8").strip()
    license_text = (root / "LICENSE").read_bytes()
    quoted_description = json.dumps(DESCRIPTION, ensure_ascii=False)
    skill = (
        f"---\nname: {SKILL_NAME}\ndescription: {quoted_description}\nlicense: MIT\n---\n\n"
        f"{approved}\n"
    )
    interface = (
        f"interface:\n  display_name: {json.dumps(SKILL_NAME, ensure_ascii=False)}\n"
        f"  short_description: {quoted_description}\n"
        "policy:\n  allow_implicit_invocation: false\n"
    )
    files = {
        f"{SKILL_NAME}/SKILL.md": skill.encode("utf-8"),
        f"{SKILL_NAME}/agents/openai.yaml": interface.encode("utf-8"),
        f"{SKILL_NAME}/LICENSE": license_text,
    }
    for name in REFERENCE_NAMES:
        files[f"{SKILL_NAME}/references/{name}"] = (
            root / "drafts/references" / name
        ).read_bytes()

    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for relative, content in sorted(files.items()):
            entry = zipfile.ZipInfo(relative, date_time=(2026, 9, 5, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(entry, content)

    skills_output = output / "skills"
    archive_output = output / "arc-9.zip"
    expected = {skills_output / relative: content for relative, content in files.items()}
    expected[archive_output] = buffer.getvalue()
    expected_directories = {
        directory
        for relative in files
        for directory in (skills_output / relative).parents
        if skills_output in directory.parents
    }
    existing_files, existing_directories = existing_outputs(output, skills_output, archive_output)
    expected_file_names = {path.parts for path in expected}
    expected_directory_names = {path.parts for path in expected_directories}
    obsolete_files = [path for path in existing_files if path.parts not in expected_file_names]
    obsolete_directories = [
        path for path in existing_directories if path.parts not in expected_directory_names
    ]
    if check:
        differences = [str(path) for path, content in expected.items()
                       if not path.is_file() or path.read_bytes() != content]
        differences += [str(path) for path in sorted(obsolete_files + obsolete_directories)]
        if differences:
            raise ValueError("Package differs from approved sources: " + ", ".join(differences))
    else:
        for path in sorted(obsolete_files):
            path.unlink()
        for path in sorted(obsolete_directories, key=lambda path: len(path.parts), reverse=True):
            path.rmdir()
        for path, content in expected.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            replace_output_file(path, content)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verify without writing")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    try:
        package(root, root / "dist", check=args.check)
    except ValueError as error:
        parser.exit(1, f"{error}\n")
    print("1 standalone skill: " + ("verified" if args.check else "packaged"))


if __name__ == "__main__":
    main()
