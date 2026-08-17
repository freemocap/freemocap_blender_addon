"""Derive a recording's true framerate from the timestamps written alongside its videos.

The addon previously assumed 30 fps (`ReduceShakiness.recording_fps`) and left the Blender
scene at its 24 fps default, so exported .blend/.fbx/.bvh carried the wrong rate and
velocity-based smoothing was computed against a framerate the recording never had.

FreeMoCap writes per-frame capture timestamps next to the synchronized videos, so the real
rate is available on disk and does not need to be guessed.
"""
import csv
import statistics
from pathlib import Path

# Recordings vary in layout between versions, so search rather than assume one path.
_TIMESTAMP_GLOBS = (
    "synchronized_videos/timestamps/*_timestamps.csv",
    "synchronized_videos/timestamps/**/*timestamps.csv",
)
_DURATION_COLUMN_HINT = "frame_duration"
_MIN_SAMPLES = 10
# Anything outside this is more likely a parsing error than a real capture rate.
_PLAUSIBLE_FPS = (1.0, 1000.0)


def _find_timestamp_csv(recording_path: Path) -> Path | None:
    for pattern in _TIMESTAMP_GLOBS:
        for candidate in sorted(recording_path.glob(pattern)):
            if candidate.is_file() and candidate.stat().st_size > 0:
                return candidate
    return None


def _median_frame_duration_ms(csv_path: Path) -> float | None:
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            return None
        columns = [c for c in reader.fieldnames if _DURATION_COLUMN_HINT in c]
        if not columns:
            return None
        column = columns[0]
        durations = []
        for row in reader:
            try:
                value = float(row[column])
            except (TypeError, ValueError):
                continue
            if value > 0:
                durations.append(value)
    if len(durations) < _MIN_SAMPLES:
        return None
    return statistics.median(durations)


def get_recording_framerate(recording_path: str | Path) -> float | None:
    """Return the recording's median framerate in fps, or None if it cannot be determined.

    Returns None rather than a default so callers can decide whether to fall back or fail -
    silently substituting a plausible-looking number is what caused the original bug.
    """
    recording_path = Path(recording_path)
    csv_path = _find_timestamp_csv(recording_path)
    if csv_path is None:
        print(f"No timestamps CSV found under {recording_path}; cannot determine framerate")
        return None

    median_ms = _median_frame_duration_ms(csv_path)
    if median_ms is None or median_ms <= 0:
        print(f"Could not read usable frame durations from {csv_path}")
        return None

    framerate = 1000.0 / median_ms
    low, high = _PLAUSIBLE_FPS
    if not (low <= framerate <= high):
        print(f"Derived implausible framerate {framerate:.2f} fps from {csv_path}; ignoring")
        return None

    print(f"Derived recording framerate: {framerate:.3f} fps (from {csv_path.name})")
    return framerate