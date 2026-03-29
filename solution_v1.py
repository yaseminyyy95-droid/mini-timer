"""
mini-timer v1
Student Name (Student ID)

V1 goals:
1. Implement a real start/stop timer flow.
2. Persist finished sessions in a log file.
3. Provide log and stats commands.

This version uses only standard library modules.
"""

import os
import sys
from datetime import datetime

DATA_DIR = ".minitimer"
ACTIVE_FILE = os.path.join(DATA_DIR, "active.txt")
SESSIONS_FILE = os.path.join(DATA_DIR, "sessions.log")


# Dizin ve dosyaları hazırlar.
def initialize():
    if os.path.exists(DATA_DIR):
        return "Already initialized"
    os.mkdir(DATA_DIR)
    open(ACTIVE_FILE, "w", encoding="utf-8").close()
    open(SESSIONS_FILE, "w", encoding="utf-8").close()
    return "Initialized empty mini-timer in .minitimer/"


# Projenin başlatılıp başlatılmadığını kontrol eder.
def ensure_initialized():
    return os.path.exists(DATA_DIR) and os.path.exists(ACTIVE_FILE) and os.path.exists(SESSIONS_FILE)


# Aktif oturumu dosyadan okur.
def read_active_session():
    if not os.path.exists(ACTIVE_FILE):
        return None
    content = open(ACTIVE_FILE, "r", encoding="utf-8").read().strip()
    if not content:
        return None
    started_at, label = content.split("|", 1)
    return {"started_at": started_at, "label": label}


# Aktif oturumu dosyaya yazar.
def write_active_session(started_at, label):
    open(ACTIVE_FILE, "w", encoding="utf-8").write(started_at + "|" + label)


# Aktif oturumu temizler.
def clear_active_session():
    open(ACTIVE_FILE, "w", encoding="utf-8").close()


# Yeni bir timer başlatır.
def start_session(label):
    if not ensure_initialized():
        return "Not initialized. Run: python solution_v1.py init"

    active = read_active_session()
    if active is not None:
        return "A timer is already running."

    started_at = datetime.now().replace(microsecond=0).isoformat()
    write_active_session(started_at, label)
    return 'Started "' + label + '" at ' + started_at


# Aktif timer'ı durdurur ve log'a yazar.
def stop_session():
    if not ensure_initialized():
        return "Not initialized. Run: python solution_v1.py init"

    active = read_active_session()
    if active is None:
        return "No active timer found."

    started_at = active["started_at"]
    label = active["label"]
    stopped_at = datetime.now().replace(microsecond=0).isoformat()

    started_dt = datetime.fromisoformat(started_at)
    stopped_dt = datetime.fromisoformat(stopped_at)
    duration_seconds = int((stopped_dt - started_dt).total_seconds())
    if duration_seconds < 0:
        duration_seconds = 0

    line = started_at + "|" + label + "|" + stopped_at + "|" + str(duration_seconds) + "\n"
    with open(SESSIONS_FILE, "a", encoding="utf-8") as f:
        f.write(line)

    clear_active_session()
    return 'Stopped "' + label + '" after ' + str(duration_seconds) + "s"


# Kayıtlı tüm oturumları listeler.
def show_log():
    if not ensure_initialized():
        return "Not initialized. Run: python solution_v1.py init"

    lines = open(SESSIONS_FILE, "r", encoding="utf-8").read().splitlines()
    if len(lines) == 0:
        return "No sessions found."

    output = []
    for index, line in enumerate(lines, start=1):
        started_at, label, stopped_at, duration = line.split("|")
        output.append(
            "[" + str(index) + "] " + label
            + " | started: " + started_at
            + " | stopped: " + stopped_at
            + " | duration: " + duration + "s"
        )
    return "\n".join(output)


# Oturum istatistiklerini hesaplar.
def show_stats():
    if not ensure_initialized():
        return "Not initialized. Run: python solution_v1.py init"

    lines = open(SESSIONS_FILE, "r", encoding="utf-8").read().splitlines()
    if len(lines) == 0:
        return "No sessions found."

    total_sessions = len(lines)
    total_duration = 0

    for line in lines:
        _, _, _, duration = line.split("|")
        total_duration += int(duration)

    average_duration = total_duration // total_sessions
    return (
        "Sessions: " + str(total_sessions) + "\n"
        + "Total duration: " + str(total_duration) + "s\n"
        + "Average duration: " + str(average_duration) + "s"
    )


# Komut satırı akışını yönetir.
def main():
    if len(sys.argv) < 2:
        print("Usage: python solution_v1.py <command> [args]")
        return

    command = sys.argv[1]

    if command == "init":
        print(initialize())
    elif command == "start":
        if len(sys.argv) < 3:
            print("Usage: python solution_v1.py start \"Study session\"")
        else:
            print(start_session(sys.argv[2]))
    elif command == "stop":
        print(stop_session())
    elif command == "log":
        print(show_log())
    elif command == "stats":
        print(show_stats())
    else:
        print("Unknown command: " + command)


if __name__ == "__main__":
    main()
