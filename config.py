"""
Configuration and color palette for the CPU Scheduling Simulator.
Modern dark dashboard style.
"""

# ──────────────────────────────────────────────────────────────
# Color Palette – Modern Dark Dashboard
# ──────────────────────────────────────────────────────────────
BG          = "#0b0b0f"      # Deep background
SIDEBAR     = "#111116"      # Sidebar background
CARD        = "#16161d"      # Card background
CARD_ALT    = "#1c1c25"      # Slightly lighter card
HOVER       = "#22222c"      # Hover state
BORDER      = "#2a2a35"      # Subtle borders

ACCENT      = "#3b82f6"      # Primary blue
ACCENT_HOVER= "#2563eb"
GREEN       = "#22c55e"
ORANGE      = "#f59e0b"
RED         = "#ef4444"
PURPLE      = "#a855f7"
CYAN        = "#06b6d4"

TEXT        = "#ffffff"
TEXT_DIM    = "#9ca3af"
TEXT_MUTED  = "#6b7280"

# Process colors for Gantt chart
PROCESS_COLORS = [
    "#3b82f6", "#22c55e", "#f59e0b", "#ef4444",
    "#a855f7", "#06b6d4", "#ec4899", "#84cc16",
    "#f97316", "#8b5cf6", "#14b8a6", "#eab308"
]

# Application settings
APP_TITLE    = "CPU Scheduling Algorithm Simulator"
APP_GEOMETRY = "1320x860"
APP_MINSIZE  = (1150, 720)

# Available algorithms
ALGORITHMS = [
    ("FCFS", "First-Come First-Served"),
    ("SJF", "Shortest Job First"),
    ("SRTF", "Shortest Remaining Time"),
    ("Priority", "Priority (Non-preemptive)"),
    ("Round Robin", "Round Robin"),
]
