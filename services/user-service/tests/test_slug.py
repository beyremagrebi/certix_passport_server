import unittest

from app.utils.slug import (
    SLUG_BASE_MAX_LENGTH,
    SLUG_FALLBACK_BASE,
    build_slug_base,
    generate_slug,
    slugify,
)


class SlugifyTests(unittest.TestCase):
    def test_strips_accents_and_lowercases(self):
        self.assertEqual(slugify("Élève Çà"), "eleve-ca")

    def test_replaces_punctuation_with_single_hyphen(self):
        self.assertEqual(slugify("O'Brien  --  Jr."), "o-brien-jr")

    def test_trims_leading_and_trailing_hyphens(self):
        self.assertEqual(slugify("  -Ali- "), "ali")


class BuildSlugBaseTests(unittest.TestCase):
    def test_joins_first_and_last_name(self):
        self.assertEqual(build_slug_base("Maki", "Test"), "maki-test")

    def test_falls_back_when_name_has_no_ascii_letters(self):
        self.assertEqual(build_slug_base("محمد", "علي"), SLUG_FALLBACK_BASE)

    def test_truncates_long_names_without_trailing_hyphen(self):
        base = build_slug_base("a" * 59 + " b", "c" * 100)
        self.assertLessEqual(len(base), SLUG_BASE_MAX_LENGTH)
        self.assertFalse(base.endswith("-"))


class GenerateSlugTests(unittest.TestCase):
    def test_format_is_name_then_six_digits(self):
        self.assertRegex(generate_slug("Maki", "Test"), r"^maki-test-\d{6}$")

    def test_only_contains_url_safe_characters(self):
        self.assertRegex(generate_slug("Élodie", "D'Arc"), r"^[a-z0-9-]+$")

    def test_fits_in_database_column(self):
        self.assertLessEqual(len(generate_slug("x" * 200, "y" * 200)), 80)

    def test_suffix_is_random(self):
        suffixes = {generate_slug("A", "B")[-6:] for _ in range(50)}
        self.assertGreater(len(suffixes), 1)


if __name__ == "__main__":
    unittest.main()
