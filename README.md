# CPU Scheduling Algorithm Simulator

Clean dark desktop application built with **pure Python + Tkinter + Matplotlib**.

## Structure

```
CPU_Scheduling_Simulator/
├── main.py                 ← Run this file
├── config.py               ← Colors & constants
├── algorithms/
│   ├── __init__.py
│   ├── metrics.py
│   ├── fcfs.py
│   ├── sjf.py
│   ├── srtf.py
│   ├── priority.py
│   └── round_robin.py
└── ui/
    ├── __init__.py
    ├── styles.py
    └── app.py
```

## Requirements

- Python 3.8+
- matplotlib 
- Tkinter

## How to run

```bash
python main.py
```

## Algorithms included

- FCFS
- SJF (Non-preemptive)
- SRTF (Preemptive)
- Priority (Non-preemptive)
- Round Robin
