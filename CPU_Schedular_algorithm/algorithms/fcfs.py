def fcfs(processes):
    processes.sort(key=lambda x: x["arrival"])
    time = 0
    gantt = []

    for p in processes:
        if time < p["arrival"]:
            time = p["arrival"]
        start = time
        time += p["burst"]
        gantt.append({"pid": p["pid"], "start": start, "end": time})

    return gantt
