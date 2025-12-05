from flask import Flask, render_template, request, jsonify
from algorithms.fcfs import fcfs
from algorithms.sjf import sjf
from algorithms.priority import priority_scheduling
from algorithms.round_robin import round_robin

app = Flask(__name__)

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

    return gantt, results, total_wt / len(processes), total_tat / len(processes)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/run", methods=["POST"])
def run():
    data = request.get_json()
    raw_processes = data["processes"]
    algo = data["algorithm"]
    quantum = int(data.get("quantum", 2))

    processes = []

    for p in raw_processes:
        processes.append({
            "pid": int(p["pid"]),
            "arrival": int(p.get("arrival") or 0),
            "burst": int(p.get("burst") or 1),
            "priority": int(p.get("priority") or 0)
        })

    if algo == "FCFS":
        gantt = fcfs(processes)
    elif algo == "SJF":
        gantt = sjf(processes)
    elif algo == "PRIORITY":
        gantt = priority_scheduling(processes)
    else:
        gantt = round_robin(processes, quantum)

    gantt, results, avg_wt, avg_tat = calculate_metrics(gantt, processes)

    return jsonify({
        "gantt": gantt,
        "results": results,
        "avg_wt": avg_wt,
        "avg_tat": avg_tat
    })


@app.route("/compare", methods=["POST"])
def compare():
    data = request.get_json()
    raw_processes = data["processes"]
    quantum = int(data.get("quantum", 2))

    processes = [{
        "pid": int(p["pid"]),
        "arrival": int(p.get("arrival") or 0),
        "burst": int(p.get("burst") or 1),
        "priority": int(p.get("priority") or 0)
    } for p in raw_processes]

    _, _, fcfs_wt, fcfs_tat = calculate_metrics(fcfs(processes.copy()), processes)
    _, _, sjf_wt, sjf_tat = calculate_metrics(sjf(processes.copy()), processes)
    _, _, pri_wt, pri_tat = calculate_metrics(priority_scheduling(processes.copy()), processes)
    _, _, rr_wt, rr_tat = calculate_metrics(round_robin(processes.copy(), quantum), processes)

    return jsonify({
        "FCFS": {"wt": fcfs_wt, "tat": fcfs_tat},
        "SJF": {"wt": sjf_wt, "tat": sjf_tat},
        "PRIORITY": {"wt": pri_wt, "tat": pri_tat},
        "RR": {"wt": rr_wt, "tat": rr_tat}
    })


if __name__ == "__main__":
    app.run(debug=True)
