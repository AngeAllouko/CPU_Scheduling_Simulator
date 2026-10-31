"""
Main Tkinter application – Modern Dark Dashboard design.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.patches import Patch
import copy

from config import *
from ui.styles import setup_styles
from algorithms import fcfs, sjf, srtf, priority, round_robin


class CPUSchedulerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry(APP_GEOMETRY)
        self.minsize(*APP_MINSIZE)
        self.configure(bg=BG)
        self.resizable(True, True)

        # Data
        self.processes = []
        self.current_algo = "FCFS"
        self.gantt_data = []
        self.metrics = {}
        self.avg_wt = 0.0
        self.avg_tat = 0.0
        self.canvas_widget = None
        self.fig = None

        setup_styles(self)
        self._build_ui()
        self._select_algorithm("FCFS")

    # ──────────────────────────────────────────────────────────
    # Helpers
    # ──────────────────────────────────────────────────────────
    def _card(self, parent, **kwargs):
        """Create a modern solid card."""
        f = tk.Frame(parent, bg=CARD, highlightbackground=BORDER,
                     highlightthickness=1, **kwargs)
        return f

    def _btn(self, parent, text, command, bg=ACCENT, fg=TEXT, width=None):
        """Primary / secondary button."""
        btn = tk.Button(
            parent, text=text, command=command,
            font=("Segoe UI", 10, "bold"),
            bg=bg, fg=fg,
            activebackground=ACCENT_HOVER, activeforeground=TEXT,
            relief="flat", bd=0, cursor="hand2",
            padx=16, pady=9
        )
        if width:
            btn.configure(width=width)
        return btn

    def _label(self, parent, text, size=9, bold=False, color=TEXT_DIM, **kw):
        weight = "bold" if bold else "normal"
        return tk.Label(parent, text=text, font=("Segoe UI", size, weight),
                        bg=parent["bg"], fg=color, **kw)

    # ──────────────────────────────────────────────────────────
    # Build UI
    # ──────────────────────────────────────────────────────────
    def _build_ui(self):
        # ── Sidebar ──
        sidebar = tk.Frame(self, bg=SIDEBAR, width=220)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # Logo / Title area
        logo_frame = tk.Frame(sidebar, bg=SIDEBAR)
        logo_frame.pack(fill="x", padx=20, pady=(24, 20))

        tk.Label(logo_frame, text="⚡", font=("Segoe UI", 20),
                 bg=SIDEBAR, fg=ACCENT).pack(side="left")
        tk.Label(logo_frame, text="CPU Scheduler", font=("Segoe UI", 13, "bold"),
                 bg=SIDEBAR, fg=TEXT).pack(side="left", padx=(8, 0))

        # Algorithms section
        self._label(sidebar, "ALGORITHMS", size=8, bold=True,
                    color=TEXT_MUTED).pack(anchor="w", padx=22, pady=(8, 6))

        self.algo_buttons = {}
        for name, desc in ALGORITHMS:
            btn = tk.Button(
                sidebar, text=f"  {name}",
                font=("Segoe UI", 11),
                bg=SIDEBAR, fg=TEXT_DIM,
                activebackground=HOVER, activeforeground=TEXT,
                relief="flat", bd=0, anchor="w",
                cursor="hand2", padx=18, pady=11,
                command=lambda n=name: self._select_algorithm(n)
            )
            btn.pack(fill="x", padx=10, pady=1)
            self.algo_buttons[name] = btn

        # Spacer
        tk.Frame(sidebar, bg=SIDEBAR).pack(fill="both", expand=True)

        # Tip at bottom
        tip = tk.Frame(sidebar, bg=CARD_ALT, highlightbackground=BORDER,
                       highlightthickness=1)
        tip.pack(fill="x", padx=14, pady=16)
        self._label(tip, "TIP", size=8, bold=True, color=ACCENT).pack(
            anchor="w", padx=12, pady=(10, 2))
        self._label(tip,
                    "Lower number = higher\npriority.",
                    size=8, color=TEXT_DIM).pack(anchor="w", padx=12, pady=(0, 10))

        # ── Main content ──
        main = tk.Frame(self, bg=BG)
        main.pack(side="left", fill="both", expand=True)

        # Top header bar
        header = tk.Frame(main, bg=BG, height=64)
        header.pack(fill="x", padx=24, pady=(16, 8))
        header.pack_propagate(False)

        self._label(header, "Hello, Scheduler 👋", size=18, bold=True,
                    color=TEXT).pack(side="left", pady=12)
        self._label(header, "Simulate CPU scheduling algorithms",
                    size=10, color=TEXT_MUTED).pack(side="left", padx=16, pady=18)

        # Content area
        content = tk.Frame(main, bg=BG)
        content.pack(fill="both", expand=True, padx=24, pady=(0, 16))

        # ── Top metrics row ──
        metrics_row = tk.Frame(content, bg=BG)
        metrics_row.pack(fill="x", pady=(0, 14))

        self.metric_cards = {}
        metric_defs = [
            ("algo", "Current Algorithm", "FCFS", ACCENT),
            ("processes", "Processes", "0", GREEN),
            ("avg_wt", "Avg Waiting Time", "—", ORANGE),
            ("avg_tat", "Avg Turnaround", "—", PURPLE),
        ]
        for key, title, value, color in metric_defs:
            card = self._card(metrics_row)
            card.pack(side="left", fill="both", expand=True,
                      padx=(0, 10) if key != "avg_tat" else 0)

            inner = tk.Frame(card, bg=CARD)
            inner.pack(fill="both", padx=16, pady=14)

            self._label(inner, title, size=8, color=TEXT_MUTED).pack(anchor="w")
            val_lbl = tk.Label(inner, text=value, font=("Segoe UI", 18, "bold"),
                               bg=CARD, fg=color)
            val_lbl.pack(anchor="w", pady=(4, 0))
            self.metric_cards[key] = val_lbl

        # ── Middle: Input + Controls ──
        mid = tk.Frame(content, bg=BG)
        mid.pack(fill="x", pady=(0, 14))

        # Process Input card
        input_card = self._card(mid)
        input_card.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self._label(input_card, "PROCESS INPUT", size=9, bold=True,
                    color=TEXT_MUTED).pack(anchor="w", padx=16, pady=(14, 10))

        form = tk.Frame(input_card, bg=CARD)
        form.pack(fill="x", padx=16)

        fields = [
            ("PID", "pid_entry", "P1"),
            ("Arrival", "arrival_entry", "0"),
            ("Burst", "burst_entry", "5"),
            ("Priority", "priority_entry", "1"),
        ]
        self.entries = {}
        for i, (label, attr, default) in enumerate(fields):
            col = tk.Frame(form, bg=CARD)
            col.grid(row=0, column=i, padx=5, sticky="ew")
            form.columnconfigure(i, weight=1)

            self._label(col, label, size=8, color=TEXT_MUTED).pack(anchor="w")
            entry = tk.Entry(
                col, font=("Segoe UI", 11),
                bg=CARD_ALT, fg=TEXT, insertbackground=TEXT,
                relief="flat", bd=0
            )
            entry.insert(0, default)
            entry.pack(fill="x", ipady=7, pady=(3, 0))
            tk.Frame(col, bg=BORDER, height=1).pack(fill="x")
            self.entries[attr] = entry

        btn_row = tk.Frame(input_card, bg=CARD)
        btn_row.pack(fill="x", padx=16, pady=(12, 16))

        self._btn(btn_row, "＋  Add Process", self._add_process).pack(side="left", padx=(0, 8))
        self._btn(btn_row, "Clear All", self._clear_all, bg=HOVER).pack(side="left")

        # Controls card
        ctrl_card = self._card(mid)
        ctrl_card.pack(side="left", fill="y")
        ctrl_card.configure(width=230)
        ctrl_card.pack_propagate(False)

        self._label(ctrl_card, "CONTROLS", size=9, bold=True,
                    color=TEXT_MUTED).pack(anchor="w", padx=16, pady=(14, 10))

        self.quantum_frame = tk.Frame(ctrl_card, bg=CARD)
        self.quantum_frame.pack(fill="x", padx=16, pady=(0, 10))

        self._label(self.quantum_frame, "Time Quantum", size=8,
                    color=TEXT_MUTED).pack(anchor="w")
        self.quantum_entry = tk.Entry(
            self.quantum_frame, font=("Segoe UI", 11),
            bg=CARD_ALT, fg=TEXT, insertbackground=TEXT,
            relief="flat", bd=0, width=10
        )
        self.quantum_entry.insert(0, "2")
        self.quantum_entry.pack(anchor="w", ipady=6, pady=(3, 0))
        tk.Frame(self.quantum_frame, bg=BORDER, height=1).pack(fill="x")

        self._btn(ctrl_card, "▶  Simulate", self._run_simulation).pack(
            fill="x", padx=16, pady=(8, 6))
        self._btn(ctrl_card, "Reset Results", self._reset_results, bg=HOVER).pack(
            fill="x", padx=16, pady=(0, 16))

        # ── Process list ──
        list_card = self._card(content)
        list_card.pack(fill="x", pady=(0, 14))

        list_header = tk.Frame(list_card, bg=CARD)
        list_header.pack(fill="x", padx=16, pady=(12, 6))
        self._label(list_header, "ADDED PROCESSES", size=9, bold=True,
                    color=TEXT_MUTED).pack(side="left")

        list_body = tk.Frame(list_card, bg=CARD)
        list_body.pack(fill="x", padx=12, pady=(0, 12))

        cols = ("pid", "arrival", "burst", "priority")
        self.process_tree = ttk.Treeview(
            list_body, columns=cols, show="headings",
            style="Dark.Treeview", height=3
        )
        for col, text, w in zip(cols, ["PID", "Arrival", "Burst", "Priority"], [90, 90, 90, 90]):
            self.process_tree.heading(col, text=text)
            self.process_tree.column(col, width=w, anchor="center")
        self.process_tree.pack(side="left", fill="x", expand=True)

        del_btn = tk.Button(
            list_body, text="✕", font=("Segoe UI", 11, "bold"),
            bg=HOVER, fg=TEXT, relief="flat", bd=0,
            width=3, cursor="hand2",
            command=self._delete_selected_process
        )
        del_btn.pack(side="right", padx=(8, 0), ipady=6)

        # ── Bottom: Results + Gantt ──
        bottom = tk.Frame(content, bg=BG)
        bottom.pack(fill="both", expand=True)

        # Results
        results_card = self._card(bottom)
        results_card.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self._label(results_card, "RESULTS TABLE", size=9, bold=True,
                    color=TEXT_MUTED).pack(anchor="w", padx=16, pady=(12, 6))

        res_frame = tk.Frame(results_card, bg=CARD)
        res_frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        res_cols = ("pid", "at", "bt", "ct", "tat", "wt", "rt")
        self.results_tree = ttk.Treeview(
            res_frame, columns=res_cols, show="headings",
            style="Dark.Treeview", height=7
        )
        headings = ["PID", "AT", "BT", "CT", "TAT", "WT", "RT"]
        widths = [58, 52, 52, 52, 52, 52, 52]
        for col, h, w in zip(res_cols, headings, widths):
            self.results_tree.heading(col, text=h)
            self.results_tree.column(col, width=w, anchor="center")
        self.results_tree.pack(fill="both", expand=True)

        # Gantt
        gantt_card = self._card(bottom)
        gantt_card.pack(side="left", fill="both", expand=True)

        self._label(gantt_card, "GANTT CHART", size=9, bold=True,
                    color=TEXT_MUTED).pack(anchor="w", padx=16, pady=(12, 4))

        self.gantt_container = tk.Frame(gantt_card, bg=CARD)
        self.gantt_container.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.gantt_placeholder = tk.Label(
            self.gantt_container,
            text="Run a simulation to generate the Gantt chart",
            font=("Segoe UI", 11), bg=CARD, fg=TEXT_MUTED
        )
        self.gantt_placeholder.pack(expand=True)

    # ──────────────────────────────────────────────────────────
    # Logic
    # ──────────────────────────────────────────────────────────
    def _select_algorithm(self, name):
        self.current_algo = name
        for algo, btn in self.algo_buttons.items():
            if algo == name:
                btn.configure(bg=ACCENT, fg=TEXT)
            else:
                btn.configure(bg=SIDEBAR, fg=TEXT_DIM)

        self.metric_cards["algo"].configure(text=name)

        if name == "Round Robin":
            self.quantum_frame.pack(fill="x", padx=16, pady=(0, 10))
        else:
            self.quantum_frame.pack_forget()

    def _add_process(self):
        try:
            pid = self.entries["pid_entry"].get().strip()
            if not pid:
                messagebox.showwarning("Input Error", "Process ID cannot be empty.")
                return
            arrival = int(self.entries["arrival_entry"].get().strip())
            burst = int(self.entries["burst_entry"].get().strip())
            priority = int(self.entries["priority_entry"].get().strip())

            if arrival < 0 or burst <= 0 or priority < 0:
                messagebox.showwarning("Input Error", "Arrival ≥ 0, Burst > 0, Priority ≥ 0.")
                return
            if any(p["id"] == pid for p in self.processes):
                messagebox.showwarning("Input Error", f"Process ID '{pid}' already exists.")
                return

            self.processes.append({
                "id": pid, "arrival": arrival,
                "burst": burst, "priority": priority
            })
            self.process_tree.insert("", "end", values=(pid, arrival, burst, priority))
            self.metric_cards["processes"].configure(text=str(len(self.processes)))

            try:
                num = int(pid[1:]) + 1 if pid.upper().startswith("P") else len(self.processes) + 1
                self.entries["pid_entry"].delete(0, "end")
                self.entries["pid_entry"].insert(0, f"P{num}")
            except Exception:
                self.entries["pid_entry"].delete(0, "end")
                self.entries["pid_entry"].insert(0, f"P{len(self.processes)+1}")

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid integers.")

    def _delete_selected_process(self):
        selected = self.process_tree.selection()
        if not selected:
            return
        item = selected[0]
        values = self.process_tree.item(item, "values")
        pid = values[0]
        self.processes = [p for p in self.processes if p["id"] != pid]
        self.process_tree.delete(item)
        self.metric_cards["processes"].configure(text=str(len(self.processes)))

    def _clear_all(self):
        self.processes.clear()
        for item in self.process_tree.get_children():
            self.process_tree.delete(item)
        self.metric_cards["processes"].configure(text="0")
        self._reset_results()

    def _reset_results(self):
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        self.metric_cards["avg_wt"].configure(text="—")
        self.metric_cards["avg_tat"].configure(text="—")
        self.gantt_data = []
        self.metrics = {}
        if self.canvas_widget:
            self.canvas_widget.get_tk_widget().destroy()
            self.canvas_widget = None
        self.gantt_placeholder.pack(expand=True)

    def _run_simulation(self):
        if not self.processes:
            messagebox.showinfo("No Processes", "Please add at least one process.")
            return

        try:
            quantum = 2
            if self.current_algo == "Round Robin":
                quantum = int(self.quantum_entry.get().strip())
                if quantum <= 0:
                    messagebox.showwarning("Input Error", "Time Quantum must be > 0.")
                    return
        except ValueError:
            messagebox.showerror("Input Error", "Time Quantum must be a positive integer.")
            return

        procs = copy.deepcopy(self.processes)

        if self.current_algo == "FCFS":
            self.gantt_data, self.metrics = fcfs(procs)
        elif self.current_algo == "SJF":
            self.gantt_data, self.metrics = sjf(procs)
        elif self.current_algo == "SRTF":
            self.gantt_data, self.metrics = srtf(procs)
        elif self.current_algo == "Priority":
            self.gantt_data, self.metrics = priority(procs)
        elif self.current_algo == "Round Robin":
            self.gantt_data, self.metrics = round_robin(procs, quantum)
        else:
            return

        self._display_results()
        self._draw_gantt()

    def _display_results(self):
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)

        total_wt = total_tat = 0
        n = len(self.metrics)
        order = [p["id"] for p in self.processes]

        for pid in order:
            if pid not in self.metrics:
                continue
            m = self.metrics[pid]
            self.results_tree.insert("", "end", values=(
                pid, m["at"], m["bt"], m["ct"], m["tat"], m["wt"], m["rt"]
            ))
            total_wt += m["wt"]
            total_tat += m["tat"]

        self.avg_wt = total_wt / n if n else 0
        self.avg_tat = total_tat / n if n else 0
        self.metric_cards["avg_wt"].configure(text=f"{self.avg_wt:.2f}")
        self.metric_cards["avg_tat"].configure(text=f"{self.avg_tat:.2f}")

    def _draw_gantt(self):
        self.gantt_placeholder.pack_forget()
        if self.canvas_widget:
            self.canvas_widget.get_tk_widget().destroy()

        if not self.gantt_data:
            self.gantt_placeholder.pack(expand=True)
            return

        self.fig = Figure(figsize=(7.2, 3.0), dpi=100)
        self.fig.patch.set_facecolor(CARD)
        ax = self.fig.add_subplot(111)
        ax.set_facecolor(CARD)

        pids = []
        for pid, _, _ in self.gantt_data:
            if pid not in pids:
                pids.append(pid)
        color_map = {pid: PROCESS_COLORS[i % len(PROCESS_COLORS)] for i, pid in enumerate(pids)}

        for pid, start, end in self.gantt_data:
            duration = end - start
            ax.barh(0.5, duration, left=start, height=0.55,
                    color=color_map[pid], edgecolor=BG, linewidth=0.7, alpha=0.95)
            if duration >= 1.1:
                ax.text(start + duration / 2, 0.5, pid,
                        ha="center", va="center", color="white",
                        fontsize=8, fontweight="bold")

        max_time = max(e for _, _, e in self.gantt_data) if self.gantt_data else 10
        ax.set_xlim(0, max_time + 0.5)
        ax.set_ylim(0, 1.1)
        ax.set_yticks([])
        ax.set_xlabel("Time", color=TEXT_DIM, fontsize=9)
        ax.tick_params(colors=TEXT_DIM, labelsize=8)
        for spine in ["top", "right", "left"]:
            ax.spines[spine].set_visible(False)
        ax.spines["bottom"].set_color(BORDER)
        ax.xaxis.grid(True, color=BORDER, linestyle="--", linewidth=0.5, alpha=0.6)
        ax.set_axisbelow(True)

        legend_elements = [Patch(facecolor=color_map[pid], label=pid) for pid in pids]
        ax.legend(handles=legend_elements, loc="upper right",
                  facecolor=CARD_ALT, edgecolor=BORDER, labelcolor=TEXT,
                  fontsize=8, framealpha=0.95)

        self.fig.tight_layout(pad=1.1)

        self.canvas_widget = FigureCanvasTkAgg(self.fig, master=self.gantt_container)
        self.canvas_widget.draw()
        self.canvas_widget.get_tk_widget().pack(fill="both", expand=True)
