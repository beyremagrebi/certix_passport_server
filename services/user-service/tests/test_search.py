import unittest

from app.utils.search import MAX_SEARCH_TERMS, escape_like, parse_search_terms


class EscapeLikeTests(unittest.TestCase):
    def test_escapes_wildcards(self):
        self.assertEqual(escape_like("100%_done"), "100\\%\\_done")

    def test_escapes_backslash_first(self):
        self.assertEqual(escape_like("a\\b"), "a\\\\b")

    def test_plain_text_is_unchanged(self):
        self.assertEqual(escape_like("maki"), "maki")


class ParseSearchTermsTests(unittest.TestCase):
    def test_splits_on_whitespace(self):
        self.assertEqual(parse_search_terms("  maki   test "), ["maki", "test"])

    def test_empty_query_gives_no_terms(self):
        self.assertEqual(parse_search_terms(""), [])

    def test_limits_the_number_of_terms(self):
        terms = parse_search_terms("a b c d e f g h")
        self.assertEqual(len(terms), MAX_SEARCH_TERMS)


if __name__ == "__main__":
    unittest.main()