from flask import Flask, render_template, request, jsonify
from collections import deque

app = Flask(__name__)

# ---------------- FCFS ----------------
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

    return calculate_metrics(gantt, processes)

# ---------------- SJF ----------------
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

    return calculate_metrics(gantt, processes)

# ---------------- PRIORITY ----------------
def priority_scheduling(processes):
    processes.sort(key=lambda x: x["arrival"])
    completed = 0
    time = 0
    gantt = []
    done = [False] * len(processes)

    while completed < len(processes):
        idx = -1
        best = 10**9

        for i, p in enumerate(processes):
            if not done[i] and p["arrival"] <= time and p["priority"] < best:
                best = p["priority"]
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

    return calculate_metrics(gantt, processes)

# ---------------- ROUND ROBIN ----------------
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

    return calculate_metrics(gantt, processes)

# ---------------- METRICS ----------------
def calculate_metrics(gantt, processes):
    results = []
    total_wt = 0
    total_tat = 0

    for p in processes:
        completion = next(g["end"] for g in gantt if g["pid"] == p["pid"])
        tat = completion - p["arrival"]
        wt = tat - p["burst"]
        results.append({**p, "waiting": wt, "turnaround": tat})
        total_wt += wt
        total_tat += tat

    return gantt, results, total_wt/len(processes), total_tat/len(processes)

# ---------------- ROUTES ----------------
@app.route("/")
def index():
    return render_template("index.html")


# ✅ SAFE /run ROUTE
@app.route("/run", methods=["POST"])
def run():
    data = request.get_json()
    raw_processes = data["processes"]
    algo = data["algorithm"]
    quantum = int(data.get("quantum", 2))

    processes = []

    for p in raw_processes:
        arrival = p.get("arrival")
        burst = p.get("burst")
        priority = p.get("priority", 0)

        if arrival is None or arrival == "":
            arrival = 0
        if burst is None or burst == "":
            burst = 1
        if priority is None or priority == "":
            priority = 0

        processes.append({
            "pid": int(p["pid"]),
            "arrival": int(arrival),
            "burst": int(burst),
            "priority": int(priority)
        })

    if algo == "FCFS":
        gantt, results, avg_wt, avg_tat = fcfs(processes)
    elif algo == "SJF":
        gantt, results, avg_wt, avg_tat = sjf(processes)
    elif algo == "PRIORITY":
        gantt, results, avg_wt, avg_tat = priority_scheduling(processes)
    else:
        gantt, results, avg_wt, avg_tat = round_robin(processes, quantum)

    return jsonify({
        "gantt": gantt,
        "results": results,
        "avg_wt": avg_wt,
        "avg_tat": avg_tat
    })


# ✅ ✅ ✅ NEW /compare ROUTE (FOR ALGORITHM COMPARISON GRAPH)
@app.route("/compare", methods=["POST"])
def compare():
    data = request.get_json()
    raw_processes = data["processes"]
    quantum = int(data.get("quantum", 2))

    processes = []

    for p in raw_processes:
        arrival = p.get("arrival") or 0
        burst = p.get("burst") or 1
        priority = p.get("priority") or 0

        processes.append({
            "pid": int(p["pid"]),
            "arrival": int(arrival),
            "burst": int(burst),
            "priority": int(priority)
        })

    _, _, fcfs_wt, fcfs_tat = fcfs(processes.copy())
    _, _, sjf_wt, sjf_tat = sjf(processes.copy())
    _, _, pri_wt, pri_tat = priority_scheduling(processes.copy())
    _, _, rr_wt, rr_tat = round_robin(processes.copy(), quantum)

    return jsonify({
        "FCFS": {"wt": fcfs_wt, "tat": fcfs_tat},
        "SJF": {"wt": sjf_wt, "tat": sjf_tat},
        "PRIORITY": {"wt": pri_wt, "tat": pri_tat},
        "RR": {"wt": rr_wt, "tat": rr_tat}
    })


if __name__ == "__main__":
    app.run(debug=True)
