import ast
import hashlib
import importlib.util
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True


ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
FIXTURES = ROOT / "tests" / "design-routing-fixtures.jsonl"
LOCK = ROOT / "design-sources.lock.json"

NEW_SKILLS = {
    "clx-algorithmic-art",
    "clx-canvas-design",
    "clx-color-expert",
    "clx-hand-drawn-diagrams",
    "clx-immersive-web",
}


class DesignAssetTests(unittest.TestCase):
    def test_public_skill_inventory_is_22_prefixed_assets(self):
        names = {path.name for path in SKILLS.iterdir() if path.is_dir()}
        self.assertEqual(22, len(names))
        self.assertTrue(NEW_SKILLS <= names)
        self.assertTrue(all(name.startswith("clx-") for name in names))

    def test_new_skills_have_matching_frontmatter_and_offline_contract(self):
        for name in NEW_SKILLS:
            text = (SKILLS / name / "SKILL.md").read_text()
            self.assertIn(f"name: {name}", text)
            self.assertIn("offline", text.lower())
            self.assertIn("do not select", text.lower())
            self.assertNotIn("npx skills add", text)
        for name in ("clx-apple-design", "clx-frontend-design"):
            self.assertTrue((SKILLS / name / "LICENSE.txt").is_file())

    def test_offline_assets_are_local_and_bounded(self):
        algorithmic = SKILLS / "clx-algorithmic-art"
        template = (algorithmic / "assets" / "offline-canvas-template.html").read_text()
        self.assertNotIn("https://", template)
        self.assertNotIn("http://", template)
        p5 = algorithmic / "assets"
        self.assertEqual("bb7f8f14b9ce2e2344ff5cd6c06f2e105eb99541ecbfec77139e2886d9c0b9ba", hashlib.sha256((p5 / "p5.min.js").read_bytes()).hexdigest())
        self.assertEqual("d075ad44977864ad119488c8f9163a2f95f6bdaff7e20057b795e15693fd90d0", hashlib.sha256((p5 / "p5.js").read_bytes()).hexdigest())
        self.assertTrue((p5 / "P5-LICENSE.txt").is_file())
        vercel = SKILLS / "clx-vercel-web-design-guidelines"
        self.assertTrue((vercel / "references" / "command.md").is_file())
        self.assertNotIn("Fetch fresh guidelines before each review", (vercel / "SKILL.md").read_text())
        frontend = SKILLS / "clx-frontend-design" / "references" / "ui-ux-pro-max"
        self.assertTrue((frontend / "scripts" / "search.py").is_file())
        help_result = subprocess.run(
            ["python3", "-B", str(frontend / "scripts" / "search.py"), "--help"],
            capture_output=True,
            text=True,
            check=True,
        )
        for option in ("--persist", "--page", "--output-dir"):
            self.assertNotIn(option, help_result.stdout)
        with tempfile.TemporaryDirectory() as temporary:
            sentinel = pathlib.Path(temporary) / "design-system" / "MASTER.md"
            sentinel.parent.mkdir()
            sentinel.write_text("unchanged")
            subprocess.run(
                ["python3", "-B", str(frontend / "scripts" / "search.py"), "finance dashboard", "--domain", "style", "--max-results", "1", "--json"],
                cwd=temporary,
                capture_output=True,
                text=True,
                check=True,
            )
            design_result = subprocess.run(
                ["python3", "-B", str(frontend / "scripts" / "search.py"), "finance dashboard", "--design-system", "--format", "markdown"],
                cwd=temporary,
                capture_output=True,
                text=True,
                check=True,
            )
            self.assertIn("# Design system evidence", design_result.stdout)
            ascii_result = subprocess.run(
                ["python3", "-B", str(frontend / "scripts" / "search.py"), "finance dashboard", "--design-system", "--format", "ascii"],
                cwd=temporary, capture_output=True, text=True, check=True,
            )
            self.assertNotEqual(design_result.stdout, ascii_result.stdout)
            low_dials = subprocess.run(
                ["python3", "-B", str(frontend / "scripts" / "search.py"), "finance dashboard", "--design-system", "--variance", "1", "--motion", "1", "--density", "1"],
                cwd=temporary, capture_output=True, text=True, check=True,
            ).stdout
            high_dials = subprocess.run(
                ["python3", "-B", str(frontend / "scripts" / "search.py"), "finance dashboard", "--design-system", "--variance", "10", "--motion", "10", "--density", "10"],
                cwd=temporary, capture_output=True, text=True, check=True,
            ).stdout
            self.assertIn("stable grid", low_dials)
            self.assertIn("bold asymmetry", high_dials)
            self.assertNotEqual(low_dials, high_dials)
            invalid_commands = (
                ["finance", "--design-system", "--json"],
                ["finance", "--variance", "10"],
                ["finance", "--project-name", "Example"],
                ["finance", "--domain", "style", "--stack", "react"],
                ["finance", "--format", "ascii"],
                ["finance", "--design-system", "--max-results", "1"],
            )
            for arguments in invalid_commands:
                invalid = subprocess.run(
                    ["python3", "-B", str(frontend / "scripts" / "search.py"), *arguments],
                    cwd=temporary, capture_output=True, text=True,
                )
                self.assertNotEqual(0, invalid.returncode, arguments)
            self.assertEqual("unchanged", sentinel.read_text())
        persistence_check = subprocess.run(
            [
                "python3", "-B", "-c",
                "import sys; sys.path.insert(0, sys.argv[1]); import design_system as d; "
                "\ntry: d.generate_design_system('test', persist=True)\nexcept ValueError: pass\nelse: raise SystemExit('persist accepted')\n"
                "try: d.persist_design_system({})\nexcept RuntimeError: pass\nelse: raise SystemExit('writer accepted')",
                str(frontend / "scripts"),
            ],
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, persistence_check.returncode, persistence_check.stderr)
        handdrawn = SKILLS / "clx-hand-drawn-diagrams" / "scripts" / "validate_excalidraw.py"
        ast.parse(handdrawn.read_text())
        immersive = SKILLS / "clx-immersive-web" / "references"
        self.assertTrue(all((immersive / name).is_file() for name in ("technology-matrix.md", "performance.md", "asset-pipeline.md")))
        self.assertEqual([], list(immersive.glob("**/SKILL.md")))

    def test_source_lock_is_pinned_and_declares_network_boundary(self):
        lock = json.loads(LOCK.read_text())
        self.assertEqual(1, lock["schema_version"])
        self.assertGreaterEqual(len(lock["sources"]), 8)
        for source in lock["sources"]:
            self.assertRegex(source["commit"], r"^[0-9a-f]{40}$")
            self.assertIn("offline", source)
            self.assertIn("redistribution", source)
        by_name = {source["name"]: source for source in lock["sources"]}
        pinned_local = {
            "ui-ux-pro-max-skill": SKILLS / "clx-frontend-design" / "references" / "ui-ux-pro-max" / "scripts" / "search.py",
            "vercel-web-interface-guidelines": SKILLS / "clx-vercel-web-design-guidelines" / "references" / "command.md",
            "skill.color-expert": SKILLS / "clx-color-expert" / "references" / "upstream-skill.md",
        }
        for name, path in pinned_local.items():
            expected = by_name[name].get("vendored_sha256", by_name[name]["sha256"])
            self.assertEqual(expected, hashlib.sha256(path.read_bytes()).hexdigest())
        uiux = by_name["ui-ux-pro-max-skill"]["vendored_files"]
        uiux_root = SKILLS / "clx-frontend-design" / "references" / "ui-ux-pro-max"
        for relative, expected in uiux.items():
            self.assertEqual(expected, hashlib.sha256((uiux_root / relative).read_bytes()).hexdigest())

    def test_excalidraw_validator_fails_closed_without_tracebacks(self):
        path = SKILLS / "clx-hand-drawn-diagrams" / "scripts" / "validate_excalidraw.py"
        spec = importlib.util.spec_from_file_location("clx_validate_excalidraw", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        fixtures = {
            "null-element": {"type": "excalidraw", "elements": [None]},
            "bad-coordinate": {"type": "excalidraw", "elements": [{"type": "rectangle", "id": "a", "x": "bad", "y": 0, "width": 10, "height": 10}]},
            "large-overlap": {"type": "excalidraw", "elements": [
                {"type": "rectangle", "id": "a", "x": 0, "y": 0, "width": 100, "height": 100},
                {"type": "rectangle", "id": "b", "x": 50, "y": 50, "width": 100, "height": 100},
            ]},
            "small-overlap": {"type": "excalidraw", "elements": [
                {"type": "rectangle", "id": "a", "x": 0, "y": 0, "width": 100, "height": 100},
                {"type": "rectangle", "id": "b", "x": 90, "y": 0, "width": 100, "height": 100},
            ]},
        }
        with tempfile.TemporaryDirectory() as temporary:
            for name, payload in fixtures.items():
                fixture = pathlib.Path(temporary) / f"{name}.excalidraw"
                fixture.write_text(json.dumps(payload))
                errors, _ = module.validate(fixture)
                self.assertTrue(errors, name)

    def test_routing_fixture_contract(self):
        rows = [json.loads(line) for line in FIXTURES.read_text().splitlines() if line]
        by_id = {row["id"]: row for row in rows}
        self.assertGreaterEqual(len(rows), 40)
        self.assertEqual(len(rows), len(by_id))
        for row in rows:
            specialist = row["specialist"]
            process_assets = row.get("process_assets", [])
            self.assertIn(specialist, [None, "frontend", "impeccable"])
            self.assertIsInstance(process_assets, list)
            self.assertEqual(len(process_assets), len(set(process_assets)))
            self.assertLessEqual(set(process_assets), {"clx-unslop"})
            self.assertLessEqual(row["subagents"], 7)
            if row["design"]:
                self.assertGreaterEqual(row["subagents"], 1)
            else:
                self.assertEqual(0, row["subagents"])
                self.assertFalse(row["apple"])
                self.assertIsNone(specialist)
                self.assertEqual([], row["helpers"])
            if row["exact_copy"]:
                self.assertIsNone(specialist)
            if row["domain"] in {"poster", "generative-art", "diagram"}:
                self.assertFalse(row["apple"])
                self.assertIsNone(specialist)
            if row["offline"]:
                self.assertFalse(row["network"])
        self.assertEqual(["clx-unslop"], by_id["D29"].get("process_assets", []))
        self.assertEqual(
            {"D29"},
            {row["id"] for row in rows if row.get("process_assets")},
        )
        unslop = (SKILLS / "clx-unslop" / "SKILL.md").read_text()
        self.assertIn("category: writing", unslop)
        self.assertIn("remove AI-sounding phrasing", unslop)


if __name__ == "__main__":
    unittest.main()
