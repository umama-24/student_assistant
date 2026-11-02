"""
test_app.py - Simple Automated Test Suite (Task 4)
Run with:
  python3 test_app.py
"""

import unittest
import os
import sys

# Import functions from app.py
from app import init_db, save_query, get_history, delete_query, generate_ai_response

class TestStudentAssistant(unittest.TestCase):
    def setUp(self):
        init_db()

    def test_1_ai_generation(self):
        """Verify AI produces structured output across modes."""
        resp = generate_ai_response("Explain recursion", "explain", "Computer Science")
        self.assertIn("Recursion", resp)
        self.assertTrue(resp.startswith("###"))
        print("\n✅ Test 1 Passed: AI generated explanation successfully.")

    def test_2_database_persistence(self):
        """Verify database saves, retrieves, and deletes records."""
        rec_id = save_query("What is Binary Search?", "explain", "Binary search is O(log N)", "CS")
        self.assertIsInstance(rec_id, int)

        history = get_history()
        self.assertTrue(any(item["id"] == rec_id for item in history))

        delete_query(rec_id)
        print("✅ Test 2 Passed: SQLite database successfully saved and retrieved record.")

if __name__ == "__main__":
    unittest.main(verbosity=2)
