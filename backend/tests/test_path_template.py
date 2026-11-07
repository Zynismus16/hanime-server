"""path_template 单元测试

运行方式（在 backend 目录下）：

    python -m unittest discover -s tests -v
"""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.utils import path_template as pt  # noqa: E402


VARS = {
    "title": "测试标题",
    "subtitle": "",
    "series": "",
    "studio": "发行商A",
    "video_type": "类型A",
    "video_id": "123",
    "tags": "标签A,标签B",
    "upload_date": "2025-06-21",
    "year": "2025",
    "month": "06",
    "day": "21",
    "date": "2025-08-01",
    "duration": "24:00",
    "quality": "1080p",
    "ext": "mp4",
}


class RenderTest(unittest.TestCase):
    def test_both_syntaxes(self):
        self.assertEqual(pt.render("{studio}-${video_id}", VARS), "发行商A-123")

    def test_unknown_variable_becomes_empty(self):
        self.assertEqual(pt.render("{title}{nope}", VARS), "测试标题")

    def test_empty_series_collapses(self):
        rel = pt.build_relative_path("{studio}/{series}", "{title}", VARS)
        self.assertEqual(rel, "发行商A/测试标题.mp4")

    def test_nested_path(self):
        rel = pt.build_relative_path("{year}/{month}", "{video_id}_{title} [{quality}]", VARS)
        self.assertEqual(rel, "2025/06/123_测试标题 [1080p].mp4")

    def test_extension_added_once(self):
        self.assertTrue(pt.build_relative_path("", "{title}", VARS).endswith(".mp4"))
        self.assertTrue(pt.build_relative_path("", "{title}.mkv", VARS).endswith(".mkv"))


class SanitizeTest(unittest.TestCase):
    def test_illegal_chars(self):
        name = pt.sanitize_segment('a/b\\c:d*e?f"g<h>i|j')
        for char in '/\\:*?"<>|':
            self.assertNotIn(char, name)

    def test_traversal_segment_is_neutralised(self):
        self.assertEqual(pt.sanitize_segment(".."), "_")
        self.assertEqual(pt.sanitize_segment("  .  "), "_")

    def test_reserved_name(self):
        self.assertTrue(pt.sanitize_filename("CON").startswith("_"))

    def test_length_limit(self):
        rel = pt.build_relative_path("", "{title}", {"title": "长" * 500})
        self.assertLessEqual(len(rel), pt.MAX_FILENAME_LEN)


class ValidateTest(unittest.TestCase):
    def test_unknown_variable_rejected(self):
        with self.assertRaises(pt.TemplateError):
            pt.validate_template("{nope}")

    def test_traversal_rejected(self):
        with self.assertRaises(pt.TemplateError):
            pt.validate_template("../../etc")

    def test_empty_sub_path_allowed(self):
        pt.validate_template("")
        pt.validate_template("{studio}/{series}")


class ResolveTest(unittest.TestCase):
    def test_resolve_inside_base(self):
        with tempfile.TemporaryDirectory() as tmp:
            rel_dir, name, abs_path = pt.resolve_target(
                Path(tmp), "{studio}", "{video_id}", VARS
            )
            self.assertEqual(rel_dir, "发行商A")
            self.assertEqual(name, "123.mp4")
            self.assertTrue(str(abs_path).startswith(tmp))

    def test_unique_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "a.mp4"
            target.write_bytes(b"1")
            self.assertEqual(pt.unique_path(target).name, "a (1).mp4")


if __name__ == "__main__":
    unittest.main()
