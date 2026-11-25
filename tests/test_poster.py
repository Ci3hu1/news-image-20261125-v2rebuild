#!/usr/bin/env python3
"""Tests for the NI25 v2 rebuild poster (mirrors the v1 suite)."""

import ast
import hashlib
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO)


def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


class TestPoster(unittest.TestCase):
    def test_determinism(self):
        """render_poster.py twice -> byte-identical entry.png."""
        import render_poster
        first = render_poster.render()
        import io
        buf1 = io.BytesIO()
        first.save(buf1, format="PNG")
        second = render_poster.render()
        buf2 = io.BytesIO()
        second.save(buf2, format="PNG")
        self.assertEqual(buf1.getvalue(), buf2.getvalue())

    def test_clearance_zero(self):
        """No text touches a border line; every label sits inside
        its shape with clearance."""
        import render_poster
        render_poster.render()
        self.assertEqual(render_poster.clearance_violations(), 0)

    def test_main_stdlib_only(self):
        """main.py imports only the standard library."""
        tree = ast.parse(open(os.path.join(REPO, "main.py")).read())
        allowed = set(sys.stdlib_module_names)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self.assertIn(alias.name.split(".")[0], allowed)
            elif isinstance(node, ast.ImportFrom):
                self.assertIn((node.module or "").split(".")[0], allowed)

    def test_main_runs_as_nobody_on_readonly_copy(self):
        """main.py runs as uid 65534 on a read-only repo copy and
        writes a byte-identical output with mode 0644."""
        with tempfile.TemporaryDirectory() as tmp:
            copy = os.path.join(tmp, "repo")
            shutil.copytree(REPO, copy,
                            ignore=shutil.ignore_patterns("__pycache__",
                                                         ".git"))
            for root, dirs, files in os.walk(copy):
                for name in dirs + files:
                    os.chmod(os.path.join(root, name), 0o555)
            os.chmod(copy, 0o555)
            os.chmod(tmp, 0o755)  # let uid 65534 traverse the temp dir
            outdir = os.path.join(tmp, "out")
            os.makedirs(outdir)
            os.chmod(outdir, 0o777)  # let uid 65534 write the output
            env = dict(os.environ, MAKEFUN_OUTPUT_DIR=outdir)
            res = subprocess.run(
                [sys.executable, os.path.join(copy, "main.py")],
                env=env, user=65534, group=65534,
                capture_output=True, text=True, timeout=60)
            self.assertEqual(res.returncode, 0, res.stderr)
            dst = os.path.join(outdir, "entry.png")
            self.assertTrue(os.path.isfile(dst))
            self.assertEqual(sha256(dst),
                             sha256(os.path.join(REPO, "entry.png")))
            self.assertEqual(stat.S_IMODE(os.stat(dst).st_mode), 0o644)

    def test_entry_is_1024_rgb(self):
        """entry.png is a 1024x1024 RGB PNG."""
        from PIL import Image
        with Image.open(os.path.join(REPO, "entry.png")) as im:
            self.assertEqual(im.size, (1024, 1024))
            self.assertEqual(im.mode, "RGB")

    def test_story_count_46(self):
        """The poster carries 46 stories: 3 heroes + 10 featured +
        33 also-on, matching the masthead count."""
        import render_poster
        total = (len(render_poster.HEROES) + len(render_poster.FEATURED)
                 + len(render_poster.ALSO_ON))
        self.assertEqual(total, 46)
        numbers = ([n for n, *_ in render_poster.HEROES]
                   + [n for n, *_ in render_poster.FEATURED]
                   + [n for n, *_ in render_poster.ALSO_ON])
        self.assertEqual(sorted(numbers), list(range(1, 47)))


if __name__ == "__main__":
    unittest.main()
