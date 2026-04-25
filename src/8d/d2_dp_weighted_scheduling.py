# D2: Weighted Interval Scheduling using Dynamic Programming. Maximises TOTAL REWARD (not job count).

# Algorithm:
#   1. Sort jobs by finish time.
#   2. For each job j, compute p(j) = the latest job that finishes before job j starts (i.e., compatible predecessor).
#   3. Define recurrence:
#        OPT(j) = max(
#            reward[j] + OPT(p(j)),   # include job j
#            OPT(j-1)                  # exclude job j
#        )
#   4. Reconstruct which jobs were chosen by tracing back through the DP table.

import csv
import os
import sys
import bisect

# Load Jobs
def load_jobs(filepath):
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


# Predecessor Function p(j)
def compute_predecessors(jobs):
    # For each job j (0-indexed in sorted order), compute p(j): the index of the latest job i such that finish[i] <= start[j].
    # Returns 0 if no such job exists (meaning no compatible predecessor).
    # Jobs must already be sorted by finish time.
    # Uses binary search for efficiency: O(n log n)
    
    finish_times = [j['finish'] for j in jobs]
    p = []

    for j_idx, job in enumerate(jobs):
        # Binary search: find rightmost finish time <= job's start
        # bisect_right finds insertion point for job['start'] in finish_times
        # We look at index j_idx only (jobs before j)
        pos = bisect.bisect_right(finish_times, job['start'], 0, j_idx)
        # pos is the count of jobs finishing at or before job['start']
        # p(j) = pos (1-indexed DP: means OPT(pos), where 0 = empty)
        p.append(pos)

    return p


# DP Algorithm
def dp_weighted_scheduling(jobs):
    # Weighted interval scheduling via bottom-up DP.

    # Args:
    #     jobs: list of job dicts (will be sorted internally)

    # Returns:
    #     opt: DP table, opt[j] = max reward using first j jobs
    #     p: predecessor array
    #     sorted_jobs: jobs sorted by finish time
    #     selected: list of selected job dicts
    #     max_reward: optimal total reward
    
    # Step 1 - Sort by finish time
    sorted_jobs = sorted(jobs, key=lambda j: j['finish'])
    n = len(sorted_jobs)

    # Step 2 - Compute predecessors
    p = compute_predecessors(sorted_jobs)

    # Step 3 - Build DP table (1-indexed; opt[0] = 0 base case)
    # opt[j] = maximum reward considering jobs 1..j
    opt = [0] * (n + 1)

    for j in range(1, n + 1):
        job = sorted_jobs[j - 1]       # convert to 0-index
        include_j = job['reward'] + opt[p[j - 1]]
        exclude_j = opt[j - 1]
        opt[j] = max(include_j, exclude_j)

    max_reward = opt[n]

    # Step 4 - Reconstruct solution
    selected = []

    def reconstruct(j):
        if j == 0:
            return
        job = sorted_jobs[j - 1]
        include_j = job['reward'] + opt[p[j - 1]]
        if include_j >= opt[j - 1]:
            selected.append(job)
            reconstruct(p[j - 1])       # jump to predecessor
        else:
            reconstruct(j - 1)          # skip this job

    reconstruct(n)
    selected.reverse()                  # restore chronological order

    return opt, p, sorted_jobs, selected, max_reward


# Main
def run_d2(filepath):
    print("-" * 60)
    print("D2 - Weighted Interval Scheduling (Maximise Reward)")
    print("-" * 60)

    jobs = load_jobs(filepath)

    # Print input
    print(f"\nAll Jobs:")
    print(f"{'Job':<8} {'Start':<8} {'Finish':<10} {'Reward'}")
    print("-" * 35)
    for j in jobs:
        print(f"{j['job_id']:<8} {j['start']:<8} {j['finish']:<10} {j['reward']}")

    # Run DP
    opt, p, sorted_jobs, selected, max_reward = dp_weighted_scheduling(jobs)
    n = len(sorted_jobs)

    # Sorted jobs + predecessors
    print(f"\nJobs sorted by finish time + predecessor p(j):")
    print(f"{'j':<5} {'Job':<8} {'Start':<8} {'Finish':<10} "
          f"{'Reward':<10} {'p(j)'}")
    print("-" * 50)
    for idx, job in enumerate(sorted_jobs):
        j_1 = idx + 1
        pred = p[idx]
        pred_name = sorted_jobs[pred - 1]['job_id'] if pred > 0 else "none"
        print(f"{j_1:<5} {job['job_id']:<8} {job['start']:<8} "
              f"{job['finish']:<10} {job['reward']:<10} "
              f"p({j_1})={pred}  ({pred_name})")

    # DP Table
    print(f"{'-'*60}")
    print("DP TABLE")
    print(f"{'-'*60}")
    print(f"\n{'j':<6} {'Job':<8} {'Reward':<10} {'p(j)':<8} "
          f"{'Include: r+OPT(p(j))':<24} {'Exclude: OPT(j-1)':<22} {'OPT(j)'}")
    print("-" * 88)

    # j=0 base case
    print(f"{'0':<6} {'-':<8} {'-':<10} {'-':<8} {'-':<24} {'-':<22} {opt[0]}")

    for idx, job in enumerate(sorted_jobs):
        j_1 = idx + 1
        pred = p[idx]
        include_v = job['reward'] + opt[pred]
        exclude_v = opt[j_1 - 1]
        chosen = "← chosen" if include_v >= exclude_v else "← chosen"
        inc_str = f"{job['reward']} + OPT({pred}) = {include_v}"
        exc_str = f"OPT({j_1-1}) = {exclude_v}"
        print(f"{j_1:<6} {job['job_id']:<8} {job['reward']:<10} "
              f"{pred:<8} {inc_str:<24} {exc_str:<22} {opt[j_1]}")

    # Reconstruction trace
    print(f"\n{'-'*60}")
    print("RECONSTRUCTION TRACE")
    print(f"{'-'*60}")

    # Re-run reconstruction with printed trace
    def reconstruct_trace(j, opt, p, sorted_jobs):
        if j == 0:
            print(f"j=0 → base case, done.")
            return
        job = sorted_jobs[j - 1]
        include_v = job['reward'] + opt[p[j - 1]]
        exclude_v = opt[j - 1]
        if include_v >= exclude_v:
            print(f"j={j} ({job['job_id']}):"
                  f"include={include_v} >= exclude={exclude_v}"
                  f"→ INCLUDE {job['job_id']}, jump to p({j})={p[j-1]}")
            reconstruct_trace(p[j - 1], opt, p, sorted_jobs)
        else:
            print(f"j={j} ({job['job_id']}):"
                  f"include={include_v} < exclude={exclude_v}"
                  f"→ exclude {job['job_id']}, move to j={j-1}")
            reconstruct_trace(j - 1, opt, p, sorted_jobs)

    reconstruct_trace(n, opt, p, sorted_jobs)

    # Final result
    selected_ids = [j['job_id'] for j in selected]
    print(f"\n{'-'*60}")
    print("DP RESULT")
    print(f"{'-'*60}")
    print(f"Selected jobs: {selected_ids}")
    print(f"Number of jobs: {len(selected)}")
    print(f"Maximum reward: {max_reward}")
    print()

    return opt, p, sorted_jobs, selected, max_reward

if __name__ == '__main__':
    DATA_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'jobs.csv')
    run_d2(DATA_PATH)