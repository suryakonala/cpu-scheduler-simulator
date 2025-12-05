def sjf(processes):
    processes.sort(key=lambda x: x["arrival"])
    completed = 0
    time = 0
    gantt = []
    done = [False] * len(processes)

    while completed < len(processes):
        idx = -1
        min_burst = 10**9

        for i, p in enumerate(processes):
            if not done[i] and p["arrival"] <= time and p["burst"] < min_burst:
                min_burst = p["burst"]
                idx = i

        if idx == -1:
            time += 1
        else:
            p = processes[idx]
            start = time
            time += p["burst"]
            gantt.append({"pid": p["pid"], "start": start, "end": time})
            done[idx] = True
            completed += 1

    return gantt
