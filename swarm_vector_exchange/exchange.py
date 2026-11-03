"""Peer-to-peer shared vector embedding memory and delta synchronizer."""
import math
from typing import Dict, List, Any, Tuple


class VectorExchange:
    def __init__(self, node_id: str):
        self.node_id = node_id
        # doc_id -> (text, vector, origin_node)
        self._vectors: Dict[str, Tuple[str, List[float], str]] = {}

    def insert(self, doc_id: str, text: str, vector: List[float]) -> None:
        self._vectors[doc_id] = (text, vector, self.node_id)

    @staticmethod
    def _cosine_similarity(v1: List[float], v2: List[float]) -> float:
        dot = sum(a * b for a, b in zip(v1, v2))
        norm1 = math.sqrt(sum(a * a for a in v1))
        norm2 = math.sqrt(sum(b * b for b in v2))
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return dot / (norm1 * norm2)

    def search(self, query_vector: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        scored = []
        for doc_id, (text, vec, origin) in self._vectors.items():
            sim = self._cosine_similarity(query_vector, vec)
            scored.append({
                "doc_id": doc_id,
                "text": text,
                "similarity": round(sim, 4),
                "origin": origin
            })
        scored.sort(key=lambda x: x["similarity"], reverse=True)
        return scored[:top_k]

    def export_deltas(self) -> Dict[str, Dict[str, Any]]:
        return {
            doc_id: {"text": t, "vector": v, "origin": orig}
            for doc_id, (t, v, orig) in self._vectors.items()
        }

    def import_deltas(self, deltas: Dict[str, Dict[str, Any]]) -> int:
        imported = 0
        for doc_id, item in deltas.items():
            if doc_id not in self._vectors:
                self._vectors[doc_id] = (item["text"], item["vector"], item["origin"])
                imported += 1
        return imported
