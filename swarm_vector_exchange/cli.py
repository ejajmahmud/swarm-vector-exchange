"""Command-line interface for Swarm Vector Exchange."""
import argparse
from .exchange import VectorExchange

def main():
    parser = argparse.ArgumentParser(description="Swarm Vector Exchange CLI")
    parser.add_argument("--demo", action="store_true", help="Demonstrate vector sharing between agents")
    args = parser.parse_args()

    agent1 = VectorExchange("agent_alpha")
    agent2 = VectorExchange("agent_beta")

    agent1.insert("doc_1", "Authentication with JWT tokens", [0.9, 0.1, 0.2])
    print("Agent Alpha embedded doc_1. Syncing to Agent Beta...")
    deltas = agent1.export_deltas()
    agent2.import_deltas(deltas)

    search_res = agent2.search([0.85, 0.15, 0.18], top_k=1)
    print("Agent Beta retrieved without re-embedding:")
    print(" ", search_res)

if __name__ == "__main__":
    main()
