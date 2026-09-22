#!/usr/bin/env python3
"""Regression tests for the V34-compatible AmigaGuide generator."""

import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "build_amigaguide", ROOT / "tools" / "build-amigaguide.py"
)
assert SPEC and SPEC.loader
BUILD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILD)


FIXTURE = """# Manual @ Home

Contact [user@example.invalid](mailto:user@example.invalid).

## First @ Section

Ordinary literal user@example.invalid remains literal.

See [Second @ Section](#second-section).

### MAIL@HOST

```text
user@example.invalid
@node is preformatted text, not a directive
```

## Second @ Section

Return to [First @ Section](#first-section).
"""


class AmigaGuideGeneratorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.guide = BUILD.convert(FIXTURE)

    def test_literal_at_characters_are_not_doubled(self) -> None:
        self.assertIn("Contact user@example.invalid.", self.guide)
        self.assertIn("Ordinary literal user@example.invalid remains literal.", self.guide)
        self.assertIn("\nuser@example.invalid\n", self.guide)
        self.assertNotIn("user@@example.invalid", self.guide)

    def test_metadata_titles_and_link_labels_keep_literal_at(self) -> None:
        self.assertIn('@database "Manual @ Home"', self.guide)
        self.assertIn('@node Main "Manual @ Home"', self.guide)
        self.assertIn('@node First_Section "First @ Section"', self.guide)
        self.assertIn('@{"First @ Section" link First_Section}', self.guide)

    def test_nodes_navigation_and_cross_references_remain_commands(self) -> None:
        self.assertIn('@node Main "Manual @ Home"', self.guide)
        self.assertIn('@node First_Section "First @ Section"', self.guide)
        self.assertIn('@node Second_Section "Second @ Section"', self.guide)
        self.assertIn('@{"Contents" link Main}', self.guide)
        self.assertIn('@{"Next" link Second_Section}', self.guide)
        self.assertIn('@{"Prev" link First_Section}', self.guide)
        self.assertIn('@{"Second @ Section" link Second_Section}', self.guide)
        self.assertIn('@{"First @ Section" link First_Section}', self.guide)

    def test_command_looking_preformatted_text_is_made_safe(self) -> None:
        self.assertIn("\n @node is preformatted text, not a directive\n", self.guide)
        self.assertEqual(self.guide.count("\n@node "), 4)

    def test_literal_attribute_opener_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "AmigaGuide 34.x"):
            BUILD.convert("# Manual\n\n## Text\n\nLiteral @{not-a-command}.\n")

    def test_structural_validator_accepts_generated_output(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            guide = Path(directory) / "fixture.guide"
            guide.write_text(self.guide, encoding="latin-1", newline="\n")
            result = subprocess.run(
                [sys.executable, str(ROOT / "tools" / "validate-amigaguide.py"), str(guide)],
                check=False,
                capture_output=True,
                text=True,
            )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("validation passed: 4 nodes", result.stdout)

    def test_structural_validator_rejects_command_looking_literal_text(self) -> None:
        unsafe = '@database "Unsafe"\n@node Main "Unsafe"\n@literal\n@endnode\n'
        with tempfile.TemporaryDirectory() as directory:
            guide = Path(directory) / "unsafe.guide"
            guide.write_text(unsafe, encoding="latin-1", newline="\n")
            result = subprocess.run(
                [sys.executable, str(ROOT / "tools" / "validate-amigaguide.py"), str(guide)],
                check=False,
                capture_output=True,
                text=True,
            )
        self.assertEqual(result.returncode, 1)
        self.assertIn("unsupported command-looking line", result.stderr)


if __name__ == "__main__":
    unittest.main()
