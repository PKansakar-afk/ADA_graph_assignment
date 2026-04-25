import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from d1_greedy_scheduling import run_d1
from d2_dp_weighted_scheduling import run_d2

JOBS = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'jobs.csv')

if __name__ == '__main__':

    print("\n" + "-" * 60)
    print("  PART D — DYNAMIC PROGRAMMING SCHEDULING")
    print("-" * 60 + "\n")

    # D1 — Greedy baseline
    jobs, greedy_selected = run_d1(JOBS)

    print("\n" + "-" * 60 + "\n")

    # D2 — Weighted DP
    opt, p, sorted_jobs, dp_selected, max_reward = run_d2(JOBS)

    # Side-by-side comparison of D1 vs D2
    print("-" * 60)
    print("D1 vs D2 — GREEDY vs DP COMPARISON")
    print("-" * 60)

    greedy_ids = [j['job_id'] for j in greedy_selected]
    dp_ids = [j['job_id'] for j in dp_selected]
    greedy_rew = sum(j['reward'] for j in greedy_selected)
    dp_rew = sum(j['reward'] for j in dp_selected)

    print(f"""
      Metric           | Greedy (D1)     | DP (D2)
      ----------------------------------------------
      Objective        | Max job count   | Max reward
      Selected jobs    | {greedy_ids}    | {dp_ids}
      Job count        | {len(greedy_selected)}               | {len(dp_selected)}
      Total reward     | {greedy_rew}              | {dp_rew}
    """)

    print("\n" + "-" * 60)
    print("  PART D COMPLETE")
    print("-" * 60 + "\n")