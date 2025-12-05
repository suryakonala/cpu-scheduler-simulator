from collections import deque

def round_robin(processes, quantum):
    processes.sort(key=lambda x: x["arrival"])
    queue = deque()
    time = 0
    gantt = []
    remaining = {p["pid"]: p["burst"] for p in processes}
    index = 0

    while queue or index < len(processes):
        if not queue and index < len(processes):
            time = max(time, processes[index]["arrival"])

        while index < len(processes) and processes[index]["arrival"] <= time:
            queue.append(processes[index])
            index += 1

        p = queue.popleft()
        exec_time = min(quantum, remaining[p["pid"]])
        start = time
        time += exec_time
        remaining[p["pid"]] -= exec_time

        gantt.append({"pid": p["pid"], "start": start, "end": time})

        while index < len(processes) and processes[index]["arrival"] <= time:
            queue.append(processes[index])
            index += 1

        if remaining[p["pid"]] > 0:
            queue.append(p)

    return gantt
