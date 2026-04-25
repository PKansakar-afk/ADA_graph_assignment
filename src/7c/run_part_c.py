import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from c1_prim import run_c1

INFRA = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'infra.csv')

if __name__ == '__main__':

    print("\n" + "-" * 60)
    print("PART C — GREEDY NETWORK DESIGN")
    print("-" * 60 + "\n")

    # C1 — Prim's MST
    run_c1(INFRA)

    print("\n" + "-" * 60)
    print("PART C COMPLETE")
    print("-" * 60 + "\n")