"""
Round Robin scheduling algorithm.
"""

from collections import deque
from .metrics import compute_metrics


def round_robin(procs, quantum):
    """
    Round Robin with given time quantum.

    Args:
        procs: list of process dicts
        quantum: positive integer time quantum

    Returns:
        (gantt_list, metrics_dict)
    """
    remaining = {p["id"]: p["burst"] for p in procs}
    arrival = {p["id"]: p["arrival"] for p in procs}
    n = len(procs)
    completed = 0
    time = 0
    gantt = []
    completion = {}
    first_response = {}

    procs_sorted = sorted(procs, key=lambda x: (x["arrival"], x["id"]))
    queue = deque()
    idx = 0
    in_queue = set()

    # Seed queue with processes that arrive at time 0
    while idx < n and procs_sorted[idx]["arrival"] <= time:
        pid = procs_sorted[idx]["id"]
        queue.append(pid)
        in_queue.add(pid)
        idx += 1

    while completed < n:
        if not queue:
            if idx < n:
                time = procs_sorted[idx]["arrival"]
                while idx < n and procs_sorted[idx]["arrival"] <= time:
                    pid = procs_sorted[idx]["id"]
                    if pid not in in_queue and remaining[pid] > 0:
                        queue.append(pid)
                        in_queue.add(pid)
                    idx += 1
            else:
                break
            continue

        pid = queue.popleft()
        in_queue.discard(pid)

        if pid not in first_response:
            first_response[pid] = time

        run = min(quantum, remaining[pid])
        start = time
        end = time + run
        gantt.append((pid, start, end))
        remaining[pid] -= run
        time = end

        # Enqueue newly arrived processes
        while idx < n and procs_sorted[idx]["arrival"] <= time:
            new_pid = procs_sorted[idx]["id"]
            if new_pid not in in_queue and remaining[new_pid] > 0:
                queue.append(new_pid)
                in_queue.add(new_pid)
            idx += 1

        if remaining[pid] > 0:
            queue.append(pid)
            in_queue.add(pid)
        else:
            completion[pid] = time
            completed += 1

    return gantt, compute_metrics(procs, completion, first_response)
