# D1: Greedy Interval Scheduling — maximise the NUMBER of non-overlapping jobs.

# Strategy:
#   - Sort jobs by FINISH TIME (earliest deadline first).
#   - Greedily select a job if it starts at or after the last selected job's finish time.
#   - This classic greedy is provably optimal for maximising job COUNT (not reward).

import csv
import os
import sys

# Load Jobs
def load_jobs(filepath):
    # Loads jobs.csv and returns a list of job dicts: { job_id, start, finish, reward }
    jobs = []
    with open(filepath, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            jobs.append({
                'job_id': row['job_id'],
                'start': int(row['start']),
                'finish': int(row['finish']),
                'reward': int(row['reward'])
            })
    return jobs

# Greedy Algorithm
def greedy_interval_scheduling(jobs):
    # Classic greedy interval scheduling. Maximises the NUMBER of non-overlapping jobs.

    # Args:
    #     jobs : list of job dicts
    # Returns:
    #     selected : list of selected job dicts (in selection order)
    
    # Step 1 - sort by finish time (earliest finish first)
    sorted_jobs = sorted(jobs, key=lambda j: j['finish'])

    selected = []
    last_finish = 0 # track when the last selected job ends

    for job in sorted_jobs:
        # A job is compatible if it starts at or after last finish
        if job['start'] >= last_finish:
            selected.append(job)
            last_finish = job['finish']

    return selected

# Main
def run_d1(filepath):
    print("-" * 60)
    print("D1 - Greedy Interval Scheduling (Maximise Job Count)")
    print("-" * 60)

    jobs = load_jobs(filepath)

    # Print all jobs 
    print(f"\nAll Jobs:")
    print(f"{'Job':<8} {'Start':<8} {'Finish':<10} {'Reward'}")
    print("-" * 35)
    for j in jobs:
        print(f"{j['job_id']:<8} {j['start']:<8} {j['finish']:<10} {j['reward']}")

    # Run greedy
    sorted_jobs = sorted(jobs, key=lambda j: j['finish'])

    print(f"\nJobs sorted by finish time:")
    print(f"{'Job':<8} {'Start':<8} {'Finish':<10} {'Reward'}")
    print("-" * 35)
    for j in sorted_jobs:
        print(f"{j['job_id']:<8} {j['start']:<8} {j['finish']:<10} {j['reward']}")

    selected = greedy_interval_scheduling(jobs)

    # Step-by-step trace
    print(f"\nGreedy Selection Trace:")
    print("-" * 50)
    last_finish = 0
    for j in sorted_jobs:
        compatible = j['start'] >= last_finish
        status = "SELECTED" if compatible else "skipped (overlaps)"
        print(f"{j['job_id']}: start={j['start']}, finish={j['finish']}"
              f"| last_finish={last_finish} → {status}")
        if compatible:
            last_finish = j['finish']

    # Result
    selected_ids = [j['job_id'] for j in selected]
    total_reward = sum(j['reward'] for j in selected)

    print(f"\n{'-'*60}")
    print(f"GREEDY RESULT")
    print(f"{'-'*60}")
    print(f"Selected jobs: {selected_ids}")
    print(f"Number of jobs: {len(selected)}")
    print(f"Total reward: {total_reward}"
          f"(not optimised — job count is the objective here)")
    print()

    return jobs, selected

if __name__ == '__main__':
    DATA_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'jobs.csv')
    run_d1(DATA_PATH)