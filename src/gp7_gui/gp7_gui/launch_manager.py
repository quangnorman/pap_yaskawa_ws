"""
LaunchManager — non-blocking subprocess manager for ros2 launch processes.

Responsibilities:
  - Start external ros2 launch processes via subprocess.Popen.
  - Stop the entire process group (parent + all children) when switching modes.
  - Fallback pkill for orphan child processes (gzserver, task_executor, etc.)
  - Capture stdout/stderr asynchronously (feeds into a signal for the UI).
  - Expose process state (idle / launching / running / failed / stopped).
  - Thread-safe: all public methods are safe to call from the Qt main thread.

Process group strategy:
  1. Start ros2 launch with os.setsid — owns its own session/PGID.
  2. On stop: SIGINT (5s) → SIGTERM (3s) → SIGKILL (1s).
  3. Fallback pkill for known orphan children that may escape the group.
"""

import os
import signal
import subprocess
import threading
from enum import Enum, auto
from typing import Optional

from PySide6 import QtCore
from PySide6.QtCore import QObject, Signal


class LaunchState(Enum):
    IDLE = auto()
    LAUNCHING = auto()
    RUNNING = auto()
    FAILED = auto()
    STOPPED = auto()


class LaunchManager(QObject):
    """Manages a single ros2 launch subprocess and all its children."""

    log_line = Signal(str)         # emitted for each stdout/stderr line
    state_changed = Signal(str)    # state name string
    launch_finished = Signal(int)  # exit code when process ends
    stop_complete = Signal()       # emitted after stop + fallback cleanup finishes

    def __init__(self, parent=None):
        super().__init__(parent)
        self._process: Optional[subprocess.Popen] = None
        self._pgid: Optional[int] = None
        self._state = LaunchState.IDLE
        self._reader_thread: Optional[threading.Thread] = None
        self._stopped_by_request = False

    # ── Properties ────────────────────────────────────────────────────────

    @property
    def state(self) -> LaunchState:
        return self._state

    @property
    def is_running(self) -> bool:
        """True only when there is an active (not-yet-exited) process."""
        return self._process is not None and self._process.poll() is None

    def _debug_state(self) -> str:
        """Snapshot of all internal state for debug logging."""
        proc = self._process
        poll_result = proc.poll() if proc else None
        return (
            f"state={self._state.name} "
            f"is_running={self.is_running} "
            f"process={proc.pid if proc else None} "
            f"poll={poll_result} "
            f"pgid={self._pgid} "
            f"stopped_by_request={self._stopped_by_request}"
        )

    # ── Public API ────────────────────────────────────────────────────────

    def launch(
        self,
        package: str,
        launch_file: str,
        launch_args: Optional[dict] = None,
    ) -> None:
        """
        Start a ros2 launch process asynchronously in its own process group.
        Safe to call after stop() — cleans up any stale previous process object.
        """
        print(f"[LM] launch() called — {self._debug_state()}")

        # Clean up any stale previous process that already exited
        if self._process is not None and self._process.poll() is not None:
            print(f"[LM] Cleaning up stale process (pid={self._process.pid}, poll={self._process.poll()})")
            self._process = None
            self._pgid = None

        if self.is_running:
            self.log_line.emit(
                f"[LaunchManager] REJECTED: already running — {self._debug_state()}"
            )
            return

        cmd = [
            "ros2", "launch",
            package,
            launch_file,
        ]
        if launch_args:
            for key, val in launch_args.items():
                cmd.extend([f"{key}:={val}"])

        self._stopped_by_request = False
        self._set_state(LaunchState.LAUNCHING)
        print(f"[LM] launch() setting state=LAUNCHING, cmd={' '.join(cmd)}")
        self.log_line.emit(f"[LaunchManager] Starting: {' '.join(cmd)}")

        def run_process():
            try:
                self._process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    preexec_fn=os.setsid,
                    env=os.environ.copy(),
                )
                self._pgid = os.getpgid(self._process.pid)
                self._set_state(LaunchState.RUNNING)
                print(f"[LM] process started pid={self._process.pid} pgid={self._pgid}")
                self._read_output()
                self._process.wait()
                exit_code = self._process.returncode
                print(f"[LM] process exited pid={self._process.pid} exit_code={exit_code} stopped_by_request={self._stopped_by_request}")
                self._process = None
                self._pgid = None
                if self._stopped_by_request:
                    self._set_state(LaunchState.STOPPED)
                elif exit_code == 0:
                    self._set_state(LaunchState.IDLE)
                else:
                    self._set_state(LaunchState.FAILED)
                self.launch_finished.emit(exit_code)
            except FileNotFoundError:
                self.log_line.emit(
                    "[LaunchManager] ERROR: 'ros2' command not found."
                )
                self._process = None
                self._pgid = None
                self._set_state(LaunchState.FAILED)
            except Exception as e:
                self.log_line.emit(f"[LaunchManager] ERROR: {e}")
                self._process = None
                self._pgid = None
                self._set_state(LaunchState.FAILED)

        self._reader_thread = threading.Thread(target=run_process, daemon=True)
        self._reader_thread.start()

    def stop(self, timeout: float = 9.0) -> None:
        """
        Stop the process group via SIGINT (5s) → SIGTERM (3s) → SIGKILL (1s),
        then run fallback pkill for known orphan children.
        Runs on a background thread so it never blocks the Qt main thread.
        Emits stop_complete when done — even if there was no process to stop.
        """
        print(f"[LM] stop() called — {self._debug_state()}")
        self.log_line.emit(f"[LaunchManager] stop() — {self._debug_state()}")

        def _do_stop():
            self._stop_internal(timeout)
            print(f"[LM] _stop_internal done — emitting stop_complete")
            self.stop_complete.emit()

        t = threading.Thread(target=_do_stop, daemon=True)
        t.start()

    def _stop_internal(self, timeout: float) -> None:
        """Blocking stop implementation — runs on background thread."""
        proc = self._process
        if proc is None or proc.poll() is not None:
            print(f"[LM] _stop_internal: no active process (poll={proc.poll() if proc else None}), setting state=STOPPED")
            self._process = None
            self._pgid = None
            self._stopped_by_request = True
            self._set_state(LaunchState.STOPPED)
            self.log_line.emit("[LaunchManager] Process already stopped (or never started).")
            return

        self._stopped_by_request = True
        print(f"[LM] _stop_internal: killing pgid={self._pgid} pid={proc.pid}")
        self.log_line.emit(f"[LaunchManager] Stopping launch process group PGID={self._pgid}...")

        # ── Stage 1: SIGINT (5s grace) ───────────────────────────────────
        self._send_sig_to_pgid(signal.SIGINT, "SIGINT")
        if self._wait_for_exit(proc, timeout=5.0):
            self.log_line.emit("[LaunchManager] Process exited after SIGINT.")
        else:
            # ── Stage 2: SIGTERM (3s grace) ──────────────────────────────
            self._send_sig_to_pgid(signal.SIGTERM, "SIGTERM")
            if self._wait_for_exit(proc, timeout=3.0):
                self.log_line.emit("[LaunchManager] Process exited after SIGTERM.")
            else:
                # ── Stage 3: SIGKILL (1s) ───────────────────────────────
                self._send_sig_to_pgid(signal.SIGKILL, "SIGKILL")
                self._wait_for_exit(proc, timeout=1.0)
                self.log_line.emit("[LaunchManager] Process killed with SIGKILL.")

        self._process = None
        self._pgid = None
        self._set_state(LaunchState.STOPPED)

        # ── Fallback: pkill known orphan children ────────────────────────
        self._fallback_cleanup()

        self.log_line.emit("[LaunchManager] Process group stopped.")

    def reset(self) -> None:
        """Return to idle state after a FAILED or STOPPED state."""
        if not self.is_running:
            self._set_state(LaunchState.IDLE)

    # ── Private ────────────────────────────────────────────────────────────

    def _set_state(self, state: LaunchState) -> None:
        self._state = state
        print(f"[LM] state -> {state.name} — {self._debug_state()}")
        self.state_changed.emit(state.name.lower())

    def _send_sig_to_pgid(self, sig: signal.Signals, label: str) -> None:
        """Send a signal to the stored process group ID."""
        pgid = self._pgid
        if pgid is None:
            self.log_line.emit(f"[LaunchManager] Cannot send {label}: no PGID stored.")
            return
        try:
            os.killpg(pgid, sig)
            self.log_line.emit(f"[LaunchManager] Sent {label} to PGID {pgid}.")
        except (ProcessLookupError, PermissionError, OSError) as e:
            self.log_line.emit(
                f"[LaunchManager] Failed to send {label} to PGID {pgid}: {e}"
            )

    def _wait_for_exit(self, proc: subprocess.Popen, timeout: float) -> bool:
        """Return True if the process exits within the timeout."""
        try:
            proc.wait(timeout=timeout)
            return True
        except subprocess.TimeoutExpired:
            return False

    def _fallback_cleanup(self) -> None:
        """
        Kill known orphan child processes that may have escaped the process group.
        """
        self.log_line.emit(
            "[LaunchManager] Fallback cleanup: killing leftover Gazebo/RViz/MoveIt/task_executor processes..."
        )
        targets = [
            "gzserver",
            "gzclient",
            "rviz2",
            "task_executor_node",
            "move_group",
        ]
        for name in targets:
            try:
                subprocess.run(
                    ["pkill", "-f", name],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    timeout=3,
                )
                self.log_line.emit(f"[LaunchManager] Fallback: pkill -f {name}")
            except subprocess.TimeoutExpired:
                self.log_line.emit(
                    f"[LaunchManager] Fallback: pkill -f {name} timed out"
                )
            except FileNotFoundError:
                pass  # pkill not available

    def _read_output(self) -> None:
        """Read subprocess output line by line, emitting each via signal."""
        proc = self._process
        if proc is None or proc.stdout is None:
            return
        try:
            for line in iter(proc.stdout.readline, ""):
                if not line:
                    break
                self.log_line.emit(line.rstrip("\n"))
        except ValueError:
            pass  # Stream closed
