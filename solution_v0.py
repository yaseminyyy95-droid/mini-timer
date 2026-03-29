"""
mini-timer v0 — Basitlestirilmis implementasyon
Ogrenci: Yasemin

Kapsam:
- init komutu calisir
- start komutu calisir
- stop, daily ve stats daha sonra gelistirilecektir

Sinirlamalar:
- for ve while donguleri kullanilmadi
- liste literal'i kullanilmadi
- temel dosya islemleri, if/else ve return mantigi kullanildi
"""

import os
import sys
from datetime import datetime


def initialize():
    """Calisma klasorunu ve gerekli veri dosyalarini olusturur."""
    if os.path.exists(".minitimer"):
        return "Already initialized"

    os.mkdir(".minitimer")

    sessions_file = open(".minitimer/sessions.dat", "w")
    sessions_file.close()

    active_file = open(".minitimer/active_session.dat", "w")
    active_file.close()

    return "Initialized empty mini-timer in .minitimer/"


def is_initialized():
    """Uygulamanin daha once baslatilip baslatilmadigini kontrol eder."""
    return os.path.exists(".minitimer")


def get_timestamp():
    """Su anki zamani SPEC formatinda yazi olarak dondurur."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_next_session_id():
    """Kayitli oturum sayisina gore bir sonraki kimligi hesaplar."""
    sessions_file = open(".minitimer/sessions.dat", "r")
    content = sessions_file.read()
    sessions_file.close()

    if content == "":
        base_count = 0
    else:
        cleaned = content.rstrip("\n")
        base_count = cleaned.count("\n") + 1

    return base_count + 1


def has_active_session():
    """Aktif oturum dosyasinda calisan bir oturum olup olmadigini kontrol eder."""
    active_file = open(".minitimer/active_session.dat", "r")
    content = active_file.read().strip()
    active_file.close()
    return content != ""


def start_session(label, planned_minutes):
    """Yeni bir aktif Pomodoro oturumu baslatir ve aktif dosyaya yazar."""
    if not is_initialized():
        return "Not initialized. Run: python solution_v0.py init"

    if label == "" or planned_minutes == "":
        return 'Usage: python solution_v0.py start "<label>" <planned_minutes>'

    if not planned_minutes.isdigit():
        return "Invalid duration: " + planned_minutes

    if int(planned_minutes) <= 0:
        return "Invalid duration: " + planned_minutes

    if has_active_session():
        return "An active session is already running."

    session_id = get_next_session_id()
    start_time = get_timestamp()
    record = (
        str(session_id)
        + "|"
        + label
        + "|"
        + planned_minutes
        + "|"
        + start_time
        + "||ACTIVE"
    )

    active_file = open(".minitimer/active_session.dat", "w")
    active_file.write(record)
    active_file.close()

    return (
        "Started session #"
        + str(session_id)
        + ": "
        + label
        + " for "
        + planned_minutes
        + " minutes"
    )


def show_not_implemented(command_name):
    """Henuz gelistirilmemis komutlar icin gecici mesaj dondurur."""
    return "Command '" + command_name + "' will be implemented in future weeks."


def main():
    """Komut satirindan gelen argumanlara gore uygun islemi calistirir."""
    if len(sys.argv) < 2:
        print("Usage: python solution_v0.py <command> [args]")
        return

    command = sys.argv[1]

    if command == "init":
        print(initialize())
        return

    if command == "start":
        if len(sys.argv) < 4:
            print('Usage: python solution_v0.py start "<label>" <planned_minutes>')
            return
        print(start_session(sys.argv[2], sys.argv[3]))
        return

    if command == "stop":
        if not is_initialized():
            print("Not initialized. Run: python solution_v0.py init")
            return
        print(show_not_implemented("stop"))
        return

    if command == "daily":
        if not is_initialized():
            print("Not initialized. Run: python solution_v0.py init")
            return
        if len(sys.argv) < 3:
            print("Usage: python solution_v0.py daily <date>")
            return
        print(show_not_implemented("daily"))
        return

    if command == "stats":
        if not is_initialized():
            print("Not initialized. Run: python solution_v0.py init")
            return
        print(show_not_implemented("stats"))
        return

    print("Unknown command: " + command)


if __name__ == "__main__":
    main()
