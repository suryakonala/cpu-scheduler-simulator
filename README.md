# 🚀 Intelligent CPU Scheduler Simulator (Web Application)

A professional **web-based CPU Scheduling Algorithm Simulator** built using **Flask, HTML, CSS, JavaScript, and Chart.js**. This project visually demonstrates how different CPU scheduling algorithms work with **real-time Gantt chart visualization** and **performance comparison graphs**.

🔗 **Live Demo:**  
👉 https://cpu-scheduler-simulator-zj42.onrender.com

🔗 **GitHub Repository:**  
👉 https://github.com/suryakonala/cpu-scheduler-simulator

---

## 📌 Features

✅ Add multiple processes dynamically  
✅ Animated **Gantt Chart Visualization**  
✅ Accurate **Waiting Time & Turnaround Time Calculation**  
✅ **Algorithm Comparison Graph (Auto-Updated)**  
✅ **Round Robin with Time Quantum**  
✅ **Preemptive & Non-Preemptive Algorithms**  
✅ Deployed as a **live web application using Render & GitHub**

---

## 📈 Implemented Algorithms

| Algorithm | Type |
|----------|------|
| FCFS (First Come First Serve) | Non-Preemptive |
| SJF (Shortest Job First) | Non-Preemptive |
| SRTF (Preemptive SJF) | ✅ Preemptive |
| Priority Scheduling | Non-Preemptive |
| Preemptive Priority Scheduling | ✅ Preemptive |
| Round Robin | Time-Sliced |

---

## 🖥️ Tech Stack

| Layer | Technology |
|------|------------|
Frontend | HTML, CSS, JavaScript |
Visualization | Chart.js |
Backend | Python Flask |
Deployment | Render |
Version Control | GitHub |

---

## 📁 Project Folder Structure
CPU_Scheduler_Simulator/
│
├── algorithms/
│ ├── fcfs.py
│ ├── sjf.py
│ ├── srtf.py
│ ├── priority.py
│ ├── priority_preemptive.py
│ └── round_robin.py
│
├── static/
│ ├── style.css
│ └── script.js
│
├── templates/
│ └── index.html
│
├── app.py
├── requirements.txt
└── README.md
