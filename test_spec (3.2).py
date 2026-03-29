"""
mini-timer v0 test scenarios
Student: Yasemin
Project: mini-timer

These tests target the current week's v0 scope:
- init is implemented
- start is implemented
- stop, daily and stats return a temporary
  'will be implemented in future weeks' message
"""
import os
import shutil
import subprocess


SCRIPT = "solution_v0.py"


def run_cmd(args):
    """Komutu calistirir ve stdout dondurur."""
    result = subprocess.run(
        ["python", SCRIPT] + list(args),
        capture_output=True,
        text=True
    )
    return result.stdout.strip()


def setup_function():
    """Her testten once temiz bir calisma ortami hazirlar."""
    if os.path.exists(".minitimer"):
        shutil.rmtree(".minitimer")


def test_init_creates_directory_and_files():
    """init komutu klasor ve veri dosyalarini olusturmalidir."""
    output = run_cmd(("init",))
    assert output == "Initialized empty mini-timer in .minitimer/"
    assert os.path.exists(".minitimer")
    assert os.path.exists(".minitimer/sessions.dat")
    assert os.path.exists(".minitimer/active_session.dat")


def test_init_when_already_initialized():
    """Ayni ortam ikinci kez init edilirse uygun mesaj donmelidir."""
    run_cmd(("init",))
    output = run_cmd(("init",))
    assert output == "Already initialized"


def test_start_creates_active_session():
    """start komutu aktif oturum dosyasina kayit yazmalidir."""
    run_cmd(("init",))
    output = run_cmd(("start", "Math", "25"))
    assert output == "Started session #1: Math for 25 minutes"
    active = open(".minitimer/active_session.dat", "r").read().strip()
    assert "|Math|25|" in active
    assert active.endswith("|ACTIVE")


def test_start_before_init_fails():
    """init oncesi start kullanimi engellenmelidir."""
    output = run_cmd(("start", "Math", "25"))
    assert output == "Not initialized. Run: python solution_v0.py init"


def test_start_invalid_duration_fails():
    """Gecersiz sure degeri hata vermelidir."""
    run_cmd(("init",))
    output = run_cmd(("start", "Math", "zero"))
    assert output == "Invalid duration: zero"


def test_start_when_active_session_exists_fails():
    """Bir aktif oturum varken ikinci start reddedilmelidir."""
    run_cmd(("init",))
    run_cmd(("start", "Math", "25"))
    output = run_cmd(("start", "Physics", "15"))
    assert output == "An active session is already running."


def test_stop_before_init_fails():
    """stop komutu init oncesi hata vermelidir."""
    output = run_cmd(("stop",))
    assert output == "Not initialized. Run: python solution_v0.py init"


def test_stop_returns_not_implemented_message_in_v0():
    """stop komutu v0 surumunde gecici mesaj dondurmelidir."""
    run_cmd(("init",))
    output = run_cmd(("stop",))
    assert output == "Command 'stop' will be implemented in future weeks."


def test_daily_before_init_fails():
    """daily komutu init oncesi kullanilamaz."""
    output = run_cmd(("daily", "2026-03-16"))
    assert output == "Not initialized. Run: python solution_v0.py init"


def test_daily_without_argument_shows_usage():
    """daily komutu tarih olmadan kullanilamaz."""
    run_cmd(("init",))
    output = run_cmd(("daily",))
    assert output == "Usage: python solution_v0.py daily <date>"


def test_daily_returns_not_implemented_message_in_v0():
    """daily komutu v0 surumunde gecici mesaj dondurmelidir."""
    run_cmd(("init",))
    output = run_cmd(("daily", "2026-03-16"))
    assert output == "Command 'daily' will be implemented in future weeks."


def test_stats_before_init_fails():
    """stats komutu init oncesi kullanilamaz."""
    output = run_cmd(("stats",))
    assert output == "Not initialized. Run: python solution_v0.py init"


def test_stats_returns_not_implemented_message_in_v0():
    """stats komutu v0 surumunde gecici mesaj dondurmelidir."""
    run_cmd(("init",))
    output = run_cmd(("stats",))
    assert output == "Command 'stats' will be implemented in future weeks."


def test_unknown_command_message():
    """Tanimsiz komutlar acik sekilde raporlanmalidir."""
    run_cmd(("init",))
    output = run_cmd(("dance",))
    assert output == "Unknown command: dance"


def test_missing_command_shows_general_usage():
    """Komut verilmezse genel kullanim mesaji gosterilmelidir."""
    result = subprocess.run(
        ["python", SCRIPT],
        capture_output=True,
        text=True
    )
    assert result.stdout.strip() == "Usage: python solution_v0.py <command> [args]"
