"""
Shared metrics calculation for all scheduling algorithms.
"""

def compute_metrics(procs, completion, first_response):
    """
    Build metrics dictionary from completion times and first response times.

    Args:
        procs: list of process dicts with keys: id, arrival, burst, priority
        completion: dict {pid: completion_time}
        first_response: dict {pid: first_cpu_time}

    Returns:
        dict {pid: {"at", "bt", "ct", "tat", "wt", "rt"}}
    """
    metrics = {}
    for p in procs:
        pid = p["id"]
        ct = completion[pid]
        tat = ct - p["arrival"]
        wt = tat - p["burst"]
        rt = first_response[pid] - p["arrival"]
        metrics[pid] = {
            "at": p["arrival"],
            "bt": p["burst"],
            "ct": ct,
            "tat": tat,
            "wt": wt,
            "rt": rt
        }
    return metrics
