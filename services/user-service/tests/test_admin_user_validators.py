import unittest

from app.models.user_role import UserRole
from app.validators.admin_user import (
    MAX_PER_PAGE,
    validate_member_filters,
    validate_member_update,
)


class ValidateMemberFiltersTests(unittest.TestCase):
    def test_defaults(self):
        filters = validate_member_filters({})
        self.assertEqual(filters["terms"], [])
        self.assertIsNone(filters["role"])
        self.assertIsNone(filters["is_active"])
        self.assertEqual(filters["page"], 1)
        self.assertEqual(filters["per_page"], 20)

    def test_parses_all_filters(self):
        filters = validate_member_filters(
            {"q": "maki test", "role": "admin", "is_active": "false",
             "page": "2", "per_page": "50"}
        )
        self.assertEqual(filters["terms"], ["maki", "test"])
        self.assertEqual(filters["role"], UserRole.ADMIN)
        self.assertIs(filters["is_active"], False)
        self.assertEqual((filters["page"], filters["per_page"]), (2, 50))

    def test_rejects_unknown_role(self):
        with self.assertRaises(ValueError):
            validate_member_filters({"role": "superuser"})

    def test_rejects_bad_is_active(self):
        with self.assertRaises(ValueError):
            validate_member_filters({"is_active": "yes"})

    def test_rejects_non_numeric_or_out_of_range_paging(self):
        for args in (
            {"page": "abc"},
            {"page": "0"},
            {"per_page": "0"},
            {"per_page": str(MAX_PER_PAGE + 1)},
        ):
            with self.subTest(args=args), self.assertRaises(ValueError):
                validate_member_filters(args)

    def test_rejects_too_long_query(self):
        with self.assertRaises(ValueError):
            validate_member_filters({"q": "x" * 101})


class ValidateMemberUpdateTests(unittest.TestCase):
    def test_accepts_role_and_is_active(self):
        changes = validate_member_update({"role": "admin", "is_active": False})
        self.assertEqual(changes, {"role": UserRole.ADMIN, "is_active": False})

    def test_returns_only_provided_fields(self):
        self.assertEqual(validate_member_update({"is_active": True}),
                         {"is_active": True})

    def test_rejects_non_object_body(self):
        for body in (None, [], "text", 5):
            with self.subTest(body=body), self.assertRaises(ValueError):
                validate_member_update(body)

    def test_rejects_empty_body(self):
        with self.assertRaises(ValueError):
            validate_member_update({})

    def test_rejects_unknown_fields(self):
        with self.assertRaises(ValueError):
            validate_member_update({"is_active": True, "email": "x@y.z"})

    def test_rejects_invalid_role_values(self):
        for role in ("root", 1, None, ["admin"], {"a": 1}):
            with self.subTest(role=role), self.assertRaises(ValueError):
                validate_member_update({"role": role})

    def test_is_active_must_be_a_real_boolean(self):
        for value in ("false", 0, 1, None):
            with self.subTest(value=value), self.assertRaises(ValueError):
                validate_member_update({"is_active": value})


if __name__ == "__main__":
    unittest.main()