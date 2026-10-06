# Local Blender add-on tests

From the add-on repository, with its existing Python environment:

```powershell
.\.venv\Scripts\python.exe -B -m tools.run_tests
```

This runs offline unit tests, discovers Blender Launcher installations, probes
their actual Blender/Python/OS/architecture, builds the appropriate packages,
and starts isolated background Blender processes. For Blender 4.2+ both legacy
and Extension packaging are tested; older builds test the legacy format.
Blender Launcher owns downloads and version management. The test runner never
updates Launcher, installs Blender, or changes your normal Blender preferences.
It reads the Windows Launcher's `library_folder` setting. A custom or non-Windows
library can be supplied explicitly:

```powershell
python -B -m tools.run_tests --launcher-library 'D:/Blender Library'
python -B -m tools.run_tests --blender 'D:/Blender Library/stable/build/blender.exe'
```

Repeat `--blender` for multiple explicit executables. Discovery checks only
`stable`, `daily`, `experimental`, and `custom` build directories, excluding
download staging and fork channels. An empty library is a failure, not a green
test run. Build-time dependency downloads require `--download-wheels`; without
that flag a missing verified wheel cache is reported as a failure. No test uses
pip or borrows core's Python environment to supply Blender dependencies.

## Shared FreeMoCap reference data

The default run consumes **both** `test_data` (222 frames) and `sample_data`
(1,108 frames). These are the accepted publications produced by core's
`freemocap.tools.datasets` workflow, not private copies of raw downloads or a
second processing pipeline maintained by the add-on.

Discovery uses `~/freemocap_data/testing/prepared`, or
`FREEMOCAP_PROVENANCE_PREPARED_ROOT` / `--prepared-root`. Each dataset's `ready.json`
must point inside its published `current` directory. Pending `replacement.json`
transactions, missing data, wrong dataset identity/frame counts, and mismatched
Parquet/calibration hashes fail the reference setup. There is no fallback to
an arbitrary raw recording or an unsuccessful processing attempt.

The runner copies the verified Parquet file into the ignored suite directory,
records `ready.json` and its software/workflow provenance, and checks the original
Parquet, calibration, publication marker, and copied Parquet hashes after testing.
Blender only reads the copy. Tests never overwrite shared prepared data, rerun
tracking, run the optional skeleton fitter, or import FreeMoCap/SkellyForge/
SkellyTracker. This follows the file-based consumer approach used by Forge's
reference tests while enforcing core's publication checks.

Acquire or refresh data through **core's own environment and commands**, from
`repos/freemocap`: `poe process-test-data` / `poe process-sample-data`.
Use core's documented recovery commands for interrupted publications. Do not
edit markers or bypass checksums to make a test pass. Dataset generation is an
explicit upstream activity, not an automatic side effect of add-on tests.

Useful scopes:

```powershell
python -B -m tools.run_tests --unit-only
python -B -m tools.run_tests --dataset test_data
python -B -m tools.run_tests --dataset sample_data
python -B -m tools.run_tests --dataset none
```

`--dataset none` explicitly excludes real recording checks; it must not be
reported as reference-data acceptance. Requested but unavailable data fails.

## What is checked

- Offline package contracts: dependency hashes, unsafe paths, wrong ABI/platform,
  package separation, namespace imports, and reproducible archives.
- Runner/data contracts: Launcher discovery, runtime selection, failed process
  reporting, Python environment isolation, publication integrity and immutability.
- Real Blender: registration, Parquet/TOML dependencies, restart and re-enable
  across process boundaries, and controlled export API dispatch.
- Animation: real evaluated positions at keyframes, existing missing-sample
  handling, and preservation after saving and reopening a `.blend`.
- Reference data: selected processing run and sensor group, descriptor basis and
  units, full frame/timestamp grid for one saved model landmark trajectory, and
  evaluation of its finite positions in Blender after millimeters-to-meters
  conversion. Fitted-skeleton channels are not substituted for model channels.

The fixture reader in `tests/blender_scene_checks.py` is **test code**, not the
production Parquet loader. These checks do not yet validate a complete recording
loader, landmark rigidification, segment orientation import, anatomical accuracy,
or equivalence of the three proposed import paths. Reports include missing new
pipeline channels explicitly; a passing trajectory-primitive test does not make
an old recording compatible with a future loader.

Logs, snapshots, generated packages, `.blend` files, JSON results and `junit.xml`
are retained in `.test-artifacts/suite-*`. Installed test packages/preferences
use short system-temp paths to avoid Windows extraction path limits and are
removed after Blender exits. A failing build does not prevent other builds from
being tested, and any failure makes the overall command exit nonzero.

## Version coverage and CI

Recommended small matrix, latest patch per series: **3.0, 3.6 LTS, 4.2 LTS,
4.5 LTS, 5.2**. Add 3.1 as a Python-transition boundary test before promising
all intermediate releases. Prioritize downloading 4.2 and 3.6, then 4.5 and 3.0.
This tests the old minimum, later legacy behavior, Extensions introduction,
action-slot animation API, and current 5.x behavior. Old versions are compatibility
targets, not recommendations for general use. Passing selected releases does
not establish every minor version or another OS/architecture.

GitHub Actions runs the offline unit suite on push, pull request and manual
dispatch across Windows, Linux and macOS, preserving reports. The workflow has
not been run remotely as part of this local change. Full Blender CI is a later
stage: provision pinned Blender builds and validated prepared dataset artifacts,
then invoke this same runner with `--blender` and `--prepared-root`. CI does not
need Blender Launcher. Keep expensive processing in core and publish its accepted
artifacts for consumers; do not import sibling repositories to generate fixtures.

Known Windows limitation: disabling and immediately re-enabling an Extension
after loading PyArrow can break Blender's wheel cleanup. The tested lifecycle
restarts Blender while disabled before re-enabling. See `DEPENDENCIES.md`.

## Local results — 2026-10-05

Nineteen unit tests passed. The full suite passed against these Launcher-managed
Windows x64 builds (these are measured versions, not inferred family coverage):

| Blender | Bundled Python | Package formats passed |
| --- | --- | --- |
| 3.0.0 | 3.9.7 | Legacy |
| 3.6.0 | 3.10.12 | Legacy |
| 4.2.0 | 3.11.7 | Legacy, Extension |
| 4.5.0 | 3.11.11 | Legacy, Extension |
| 5.2.2 | 3.13.13 | Legacy, Extension |

All eight package combinations checked both accepted reference publications:
222 test frames (216 finite pelvis positions) and 1,108 sample frames (1,076 finite
pelvis positions), selected run 0, sensor group `camera_group:8491d7`. Original
files remained unchanged. Both publications lack `MAPPED_KEYPOINTS_3D`; reports
identify that prerequisite gap without relabeling old landmarks as mapped points.
These are trajectory-primitive and packaging checks, not complete loader acceptance.

The complete local evidence is retained in
`.test-artifacts/suite-m0o9pmni/summary.json`, `junit.xml`, and per-build logs/scenes.
