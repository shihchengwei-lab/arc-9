import importlib.util
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = "masters-lens"


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
            with zipfile.ZipFile(output / "masters-lenses.zip") as archive:
                expected_paths = {
                    f"{SKILL}/{relative}"
                    for relative in ("SKILL.md", "agents/openai.yaml", "LICENSE")
                }
                self.assertEqual(set(archive.namelist()), expected_paths)
                self.assertEqual(len(archive.namelist()), len(expected_paths))
                self.assertEqual(
                    {path.name for path in (output / "skills").iterdir()}, {SKILL}
                )
                for relative in ("SKILL.md", "agents/openai.yaml", "LICENSE"):
                    self.assertEqual(
                        archive.read(f"{SKILL}/{relative}"),
                        (output / f"skills/{SKILL}/{relative}").read_bytes(),
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
            self.packager.package(ROOT, output)
            target = output / f"skills/{SKILL}/SKILL.md"
            target.write_text("unexpected manual edit", encoding="utf-8")
            with self.assertRaises(ValueError):
                self.packager.package(ROOT, output, check=True)
            self.assertEqual(target.read_text(encoding="utf-8"), "unexpected manual edit")

    def test_check_detects_legacy_skill_without_deleting_it(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            self.packager.package(ROOT, output)
            target = output / "skills/structure/SKILL.md"
            target.parent.mkdir()
            target.write_text("obsolete skill", encoding="utf-8")
            with self.assertRaises(ValueError):
                self.packager.package(ROOT, output, check=True)
            self.assertEqual(target.read_text(encoding="utf-8"), "obsolete skill")
            target.unlink()
            with self.assertRaises(ValueError):
                self.packager.package(ROOT, output, check=True)
            self.assertTrue(target.parent.is_dir())

    def test_rebuild_removes_obsolete_outputs_and_matches_archive(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            legacy = output / "skills/boundary/agents/openai.yaml"
            legacy.parent.mkdir(parents=True)
            legacy.write_text("obsolete policy", encoding="utf-8")
            (output / "skills/structure").mkdir()
            (output / "skills/evidence").mkdir()
            extra = output / f"skills/{SKILL}/old.txt"
            extra.parent.mkdir()
            extra.write_text("obsolete file", encoding="utf-8")
            other_output = output / "notes.txt"
            other_output.write_text("keep this", encoding="utf-8")

            self.packager.package(ROOT, output)
            self.packager.package(ROOT, output, check=True)

            self.assertEqual(
                {path.name for path in (output / "skills").iterdir()}, {SKILL}
            )
            self.assertFalse(extra.exists())
            self.assertEqual(other_output.read_text(encoding="utf-8"), "keep this")
            with zipfile.ZipFile(output / "masters-lenses.zip") as archive:
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
            archive = output / "masters-lenses.zip"
            original = archive.read_bytes()
            self.packager.package(ROOT, output)
            self.assertEqual(original, archive.read_bytes())
            archive.write_bytes(b"broken archive")
            with self.assertRaises(ValueError):
                self.packager.package(ROOT, output, check=True)


if __name__ == "__main__":
    unittest.main()
