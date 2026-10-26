"""
Shortest Remaining Time First (SRTF) – Preemptive SJF.
"""

from .metrics import compute_metrics


def srtf(procs):
    """
    Preemptive Shortest Remaining Time First.

    Args:
        procs: list of process dicts

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
    current = None
    last_switch = 0

    max_time = max(p["arrival"] for p in procs) + sum(p["burst"] for p in procs) + 5

    while completed < n and time <= max_time:
        ready = [pid for pid in remaining if arrival[pid] <= time and remaining[pid] > 0]

        if not ready:
            time += 1
            continue

        # Shortest remaining time, then arrival, then pid
        ready.sort(key=lambda pid: (remaining[pid], arrival[pid], pid))
        next_p = ready[0]

        if current != next_p:
            if current is not None and time > last_switch:
                gantt.append((current, last_switch, time))
            current = next_p
            last_switch = time
            if current not in first_response:
                first_response[current] = time

        remaining[current] -= 1
        time += 1

        if remaining[current] == 0:
            completion[current] = time
            completed += 1
            gantt.append((current, last_switch, time))
            current = None
            last_switch = time

    if current is not None and time > last_switch:
        gantt.append((current, last_switch, time))

    return gantt, compute_metrics(procs, completion, first_response)
