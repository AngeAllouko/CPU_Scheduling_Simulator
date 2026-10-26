#!/usr/bin/env python3
"""
CPU Scheduling Algorithm Simulator
Entry point.

Run with:
    python main.py
"""

from ui.app import CPUSchedulerApp


def main():
    app = CPUSchedulerApp()
    app.mainloop()


if __name__ == "__main__":
    main()
