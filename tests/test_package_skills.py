import importlib.util
import os
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = "arc9"
PACKAGE_FILES = (
    "SKILL.md", "agents/openai.yaml", "LICENSE",
    "references/review.md", "references/output.md",
)


class PackagingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("packager", ROOT / "scripts/package_skills.py")
        cls.packager = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.packager)

    def test_standalone_archive_contains_approved_content_and_manual_policy(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            self.packager.package(ROOT, output)
            with zipfile.ZipFile(output / "arc-9.zip") as archive:
                expected_paths = {
                    f"{SKILL}/{relative}"
                    for relative in PACKAGE_FILES
                }
                self.assertEqual(set(archive.namelist()), expected_paths)
                self.assertEqual(len(archive.namelist()), len(expected_paths))
                self.assertEqual(
                    {path.name for path in (output / "skills").iterdir()}, {SKILL}
                )
                for relative in PACKAGE_FILES:
                    self.assertEqual(
                        archive.read(f"{SKILL}/{relative}"),
                        (output / f"skills/{SKILL}/{relative}").read_bytes(),
                    )
                for name in ("review.md", "output.md"):
                    self.assertEqual(
                        archive.read(f"{SKILL}/references/{name}"),
                        (ROOT / "drafts/references" / name).read_bytes(),
                    )
                expected_license = (ROOT / "LICENSE").read_bytes()
                self.assertEqual(archive.read(f"{SKILL}/LICENSE"), expected_license)
                body = archive.read(f"{SKILL}/SKILL.md").decode("utf-8")
                self.assertIn("\nlicense: MIT\n", body)
                approved = (ROOT / f"drafts/{SKILL}.md").read_text(encoding="utf-8").strip()
                self.assertEqual(body.split("\n---\n", 1)[1].strip(), approved)
                policy = archive.read(f"{SKILL}/agents/openai.yaml").decode("utf-8")
                self.assertIn("allow_implicit_invocation: false", policy)

    def test_check_detects_edited_skill_without_overwriting_it(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            for relative in ("SKILL.md", "references/review.md", "references/output.md"):
                with self.subTest(relative=relative):
                    self.packager.package(ROOT, output)
                    target = output / f"skills/{SKILL}" / relative
                    target.write_text("unexpected manual edit", encoding="utf-8")
                    with self.assertRaises(ValueError):
                        self.packager.package(ROOT, output, check=True)
                    self.assertEqual(
                        target.read_text(encoding="utf-8"), "unexpected manual edit"
                    )

    def test_missing_reference_prevents_build_without_changing_existing_package(self):
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "source"
            output = Path(temporary) / "output"
            for relative in (
                f"drafts/{SKILL}.md", "LICENSE",
                "drafts/references/review.md", "drafts/references/output.md",
            ):
                target = source / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes((ROOT / relative).read_bytes())
            self.packager.package(source, output)
            original = {
                path.relative_to(output): path.read_bytes()
                for path in output.rglob("*") if path.is_file()
            }
            (source / "drafts/references/review.md").unlink()
            with self.assertRaises(FileNotFoundError):
                self.packager.package(source, output)
            self.assertEqual(original, {
                path.relative_to(output): path.read_bytes()
                for path in output.rglob("*") if path.is_file()
            })

    def test_check_detects_obsolete_outputs_without_deleting_them(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            for relative in ("masters-lens/SKILL.md", f"{SKILL}/obsolete/scenes.md"):
                with self.subTest(relative=relative):
                    self.packager.package(ROOT, output)
                    target = output / "skills" / relative
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_text("obsolete output", encoding="utf-8")
                    with self.assertRaises(ValueError):
                        self.packager.package(ROOT, output, check=True)
                    self.assertEqual(target.read_text(encoding="utf-8"), "obsolete output")
                    target.unlink()
                    with self.assertRaises(ValueError):
                        self.packager.package(ROOT, output, check=True)
                    self.assertTrue(target.parent.is_dir())

    def test_rebuild_removes_obsolete_outputs_and_matches_archive(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            legacy = output / "skills/masters-lens/agents/openai.yaml"
            legacy.parent.mkdir(parents=True)
            legacy.write_text("obsolete policy", encoding="utf-8")
            (output / "skills/structure").mkdir()
            (output / "skills/evidence").mkdir()
            extra = output / f"skills/{SKILL}/old.txt"
            extra.parent.mkdir()
            extra.write_text("obsolete file", encoding="utf-8")
            old_scene = output / f"skills/{SKILL}/references/scenes.md"
            old_scene.parent.mkdir()
            old_scene.write_text("obsolete scene library", encoding="utf-8")
            other_output = output / "notes.txt"
            other_output.write_text("keep this", encoding="utf-8")
            self.packager.package(ROOT, output)
            self.packager.package(ROOT, output, check=True)

            self.assertEqual(
                {path.name for path in (output / "skills").iterdir()}, {SKILL}
            )
            self.assertFalse(extra.exists())
            self.assertFalse(old_scene.exists())
            self.assertTrue(old_scene.parent.is_dir())
            self.assertEqual(other_output.read_text(encoding="utf-8"), "keep this")
            with zipfile.ZipFile(output / "arc-9.zip") as archive:
                disk_files = {
                    path.relative_to(output / "skills").as_posix(): path.read_bytes()
                    for path in (output / "skills").rglob("*") if path.is_file()
                }
                self.assertEqual(set(archive.namelist()), set(disk_files))
                for relative, content in disk_files.items():
                    self.assertEqual(archive.read(relative), content)

    def test_check_detects_changed_archive_and_build_is_repeatable(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            self.packager.package(ROOT, output)
            archive = output / "arc-9.zip"
            original = archive.read_bytes()
            self.packager.package(ROOT, output)
            self.assertEqual(original, archive.read_bytes())
            archive.write_bytes(b"broken archive")
            with self.assertRaises(ValueError):
                self.packager.package(ROOT, output, check=True)

    @unittest.skipUnless(os.name == "nt", "requires Windows directory junctions")
    def test_package_rejects_output_junctions_before_changing_any_files(self):
        from _winapi import CreateJunction

        for linked_path in ("parent", "dist", "dist/skills", f"dist/skills/{SKILL}/references"):
            for check in (True, False):
                with self.subTest(linked_path=linked_path, check=check), tempfile.TemporaryDirectory() as temporary:
                    fixture = Path(temporary)
                    outside = fixture / "outside"
                    outside.mkdir()
                    sentinel = outside / "keep.txt"
                    sentinel.write_bytes(b"keep this")
                    if linked_path == "parent":
                        junction = fixture / "parent"
                        output = junction / "dist"
                    else:
                        junction = fixture / linked_path
                        output = fixture / "dist"
                    junction.parent.mkdir(parents=True, exist_ok=True)
                    obsolete = output / "skills/obsolete.txt"
                    if junction in obsolete.parents:
                        obsolete = None
                    else:
                        obsolete.write_bytes(b"leave this on rejection")

                    CreateJunction(str(outside), str(junction))
                    try:
                        with self.assertRaisesRegex(ValueError, "linked path"):
                            self.packager.package(ROOT, output, check=check)
                        self.assertEqual(set(outside.iterdir()), {sentinel})
                        self.assertEqual(sentinel.read_bytes(), b"keep this")
                        if obsolete is not None:
                            self.assertEqual(obsolete.read_bytes(), b"leave this on rejection")
                    finally:
                        junction.rmdir()

    def test_rebuild_replaces_hard_linked_outputs_without_overwriting_external_files(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = Path(temporary)
            output = fixture / "dist"
            self.packager.package(ROOT, output)
            archive = output / "arc-9.zip"
            skill = output / f"skills/{SKILL}/SKILL.md"
            sentinels = {archive: fixture / "outside.zip", skill: fixture / "outside.md"}
            for target, sentinel in sentinels.items():
                sentinel.write_bytes(b"keep this")
                target.unlink()
                os.link(sentinel, target)

            with self.assertRaises(ValueError):
                self.packager.package(ROOT, output, check=True)
            for target, sentinel in sentinels.items():
                self.assertTrue(target.samefile(sentinel))

            self.packager.package(ROOT, output)
            self.packager.package(ROOT, output, check=True)
            for target, sentinel in sentinels.items():
                self.assertEqual(sentinel.read_bytes(), b"keep this")
                self.assertFalse(target.samefile(sentinel))

    @unittest.skipUnless(os.name == "nt", "requires exact Windows paths")
    def test_package_rejects_names_that_win32_would_rewrite(self):
        from _winapi import CreateJunction

        with tempfile.TemporaryDirectory() as temporary:
            fixture = Path(temporary)
            output = fixture / "dist"
            self.packager.package(ROOT, output)
            skill = output / f"skills/{SKILL}/SKILL.md"
            original_skill = skill.read_bytes()
            obsolete = skill.parent / "obsolete.txt"
            obsolete.write_bytes(b"leave this on rejection")
            outside = fixture / "outside"
            outside.mkdir()
            sentinel = outside / "keep.txt"
            sentinel.write_bytes(b"keep this")
            exact_output = Path("\\\\?\\" + str(output))
            skill_dir = f"skills/{SKILL}"

            for relative, junction in (
                (f"{skill_dir}/SKILL.md.", False),
                (f"{skill_dir}/SKILL.md..", False),
                (f"{skill_dir}/SKILL.md ", False),
                (f"{skill_dir}/references.", True),
                ("arc-9.zip.", False),
                ("arc-9.zip ", False),
                ("skills.", True),
            ):
                with self.subTest(relative=relative):
                    entry = exact_output / relative
                    if junction:
                        CreateJunction(str(outside), str(entry))
                    else:
                        entry.write_bytes(b"ambiguous name")
                    try:
                        for check in (True, False):
                            with self.assertRaisesRegex(ValueError, "ambiguous Windows name"):
                                self.packager.package(ROOT, output, check=check)
                        self.assertEqual(skill.read_bytes(), original_skill)
                        self.assertEqual(obsolete.read_bytes(), b"leave this on rejection")
                        self.assertEqual(set(outside.iterdir()), {sentinel})
                        self.assertEqual(sentinel.read_bytes(), b"keep this")
                        if junction:
                            self.assertTrue(entry.is_dir())
                        else:
                            self.assertEqual(entry.read_bytes(), b"ambiguous name")
                    finally:
                        if junction:
                            entry.rmdir()
                        else:
                            entry.unlink()

    def test_check_detects_wrong_case_and_rebuild_restores_package_names(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            self.packager.package(ROOT, output)
            skills = output / "skills"
            misnamed = skills / SKILL.upper()
            (skills / SKILL).rename(skills / "renamed").rename(misnamed)
            (misnamed / "SKILL.md").rename(misnamed / "renamed.md").rename(misnamed / "skill.md")

            with self.assertRaisesRegex(ValueError, "Package differs"):
                self.packager.package(ROOT, output, check=True)
            self.packager.package(ROOT, output)
            self.packager.package(ROOT, output, check=True)
            self.assertEqual({path.name for path in skills.iterdir()}, {SKILL})
            self.assertIn("SKILL.md", {path.name for path in (skills / SKILL).iterdir()})


if __name__ == "__main__":
    unittest.main()
