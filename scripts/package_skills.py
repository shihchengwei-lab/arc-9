"""Build the standalone skill from its approved source."""

import argparse
import io
import json
import zipfile
from pathlib import Path


SKILL_NAME = "arc9"
REFERENCE_NAMES = ("review.md", "output.md")
DESCRIPTION = "使用者呼叫 arc9 濾鏡時，以唯讀方式依任務材料審查方案、說明未知並提出必要改動建議。"


def package(root, output, check=False):
    root, output = Path(root), Path(output)
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

    expected = {output / "skills" / relative: content for relative, content in files.items()}
    expected[output / "arc-9.zip"] = buffer.getvalue()
    skills_output = output / "skills"
    expected_directories = {
        directory
        for relative in files
        for directory in (skills_output / relative).parents
        if skills_output in directory.parents
    }
    existing_paths = set(skills_output.rglob("*"))
    if any(not path.resolve().is_relative_to(skills_output.resolve())
           for path in existing_paths):
        raise ValueError("Package output escapes skills directory")
    existing_paths.update(
        path for path in (output / "arc-9.zip", output / "masters-lenses.zip")
        if path.exists()
    )
    obsolete_files = {path for path in existing_paths if path.is_file()} - set(expected)
    obsolete_directories = {
        path for path in existing_paths if path.is_dir()
    } - expected_directories
    if check:
        differences = [str(path) for path, content in expected.items()
                       if not path.is_file() or path.read_bytes() != content]
        differences += [str(path) for path in sorted(obsolete_files | obsolete_directories)]
        if differences:
            raise ValueError("Package differs from approved sources: " + ", ".join(differences))
    else:
        for path in sorted(obsolete_files):
            path.unlink()
        for path in sorted(obsolete_directories, key=lambda path: len(path.parts), reverse=True):
            path.rmdir()
        for path, content in expected.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)


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
