"""
First-Come First-Served (FCFS) scheduling algorithm.
"""

from .metrics import compute_metrics


def fcfs(procs):
    """
    Non-preemptive FCFS.

    Args:
        procs: list of process dicts

    Returns:
        (gantt_list, metrics_dict)
        gantt_list = [(pid, start, end), ...]
    """
    procs = sorted(procs, key=lambda x: (x["arrival"], x["id"]))
    time = 0
    gantt = []
    completion = {}
    first_response = {}

    for p in procs:
        if time < p["arrival"]:
            time = p["arrival"]
        start = time
        if p["id"] not in first_response:
            first_response[p["id"]] = start
        end = start + p["burst"]
        gantt.append((p["id"], start, end))
        completion[p["id"]] = end
        time = end

    return gantt, compute_metrics(procs, completion, first_response)
