"""Unit tests for VectorExchange."""
import unittest
from swarm_vector_exchange.exchange import VectorExchange

class TestVectorExchange(unittest.TestCase):
    def test_search_similarity(self):
        ex = VectorExchange("n1")
        ex.insert("d1", "exact match", [1.0, 0.0])
        ex.insert("d2", "orthogonal", [0.0, 1.0])
        res = ex.search([1.0, 0.0], top_k=1)
        self.assertEqual(res[0]["doc_id"], "d1")
        self.assertAlmostEqual(res[0]["similarity"], 1.0)

    def test_sync_between_peers(self):
        ex1 = VectorExchange("n1")
        ex2 = VectorExchange("n2")
        ex1.insert("d1", "text", [0.5, 0.5])
        imported = ex2.import_deltas(ex1.export_deltas())
        self.assertEqual(imported, 1)
        self.assertEqual(len(ex2.search([0.5, 0.5])), 1)

if __name__ == "__main__":
    unittest.main()
