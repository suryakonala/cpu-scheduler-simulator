def srtf(processes):
    n = len(processes)
    remaining = {p["pid"]: p["burst"] for p in processes}

    time = 0
    completed = 0
    gantt = []

    while completed < n:
        current = None
        min_remaining = 10**9

        for p in processes:
            if p["arrival"] <= time and remaining[p["pid"]] > 0:
                if remaining[p["pid"]] < min_remaining:
                    min_remaining = remaining[p["pid"]]
                    current = p

        if current is None:
            time += 1
            continue

        start = time
        time += 1
        remaining[current["pid"]] -= 1
        end = time

        if gantt and gantt[-1]["pid"] == current["pid"]:
            gantt[-1]["end"] = end
        else:
            gantt.append({
                "pid": current["pid"],
                "start": start,
                "end": end
            })

        if remaining[current["pid"]] == 0:
            completed += 1

    return gantt
