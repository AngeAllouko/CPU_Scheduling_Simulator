"""
Shortest Job First (SJF) – Non-preemptive.
"""

from .metrics import compute_metrics


def sjf(procs):
    """
    Non-preemptive Shortest Job First.

    Args:
        procs: list of process dicts

    Returns:
        (gantt_list, metrics_dict)
    """
    completed = set()
    time = 0
    gantt = []
    completion = {}
    first_response = {}
    n = len(procs)

    while len(completed) < n:
        ready = [p for p in procs if p["arrival"] <= time and p["id"] not in completed]
        if not ready:
            next_arr = min(p["arrival"] for p in procs if p["id"] not in completed)
            time = next_arr
            continue

        # Pick shortest burst, then earliest arrival, then id
        ready.sort(key=lambda x: (x["burst"], x["arrival"], x["id"]))
        p = ready[0]
        start = time
        if p["id"] not in first_response:
            first_response[p["id"]] = start
        end = start + p["burst"]
        gantt.append((p["id"], start, end))
        completion[p["id"]] = end
        completed.add(p["id"])
        time = end

    return gantt, compute_metrics(procs, completion, first_response)
