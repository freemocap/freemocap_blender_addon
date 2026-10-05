# Self contained Blender packages

## Plan and boundaries

One source tree serves standalone use and FreeMoCap-launched export. Build two
distribution formats: Blender Extensions for 4.2 and newer, and legacy add-ons
for 3.0 through 4.1. Select binary dependencies by Python ABI, OS and architecture,
not merely the Blender version. A declared target is not a tested target.

Extensions bundle unmodified wheels in their manifest. Blender manages their
installation. No add-on code runs pip, ensurepip, Git, downloads, or installs
dependencies. Legacy Blender lacks wheel management: its separate package contains
build-time-expanded dependencies and a legacy-only import bridge. That bridge is
excluded from Extension packages and is not claimed to satisfy Extension rules.

Preserve the existing code license. Do not claim official marketplace readiness:
license/asset provenance and the remaining application behavior need separate review.

Stage 1, this repository: relative imports, dependency loading, reproducible package
builder, standalone/background registration and a shared export entry point.
Stage 2, after the human commits and pushes this repository: change FreeMoCap to
invoke the installed package's entry point instead of injecting its environment.
Stage 3: implement the three Parquet/legacy data paths described in the workspace
handoff. This stage does not implement the new landmark/segment scene loader.

The export caller must supply the exact installed package name. For Extensions,
that includes the repository namespace chosen by Blender; never hard-code it.
Both entry points use the same code and dependencies. Installation is a separate,
explicit user action, not a side effect of importing data or registering the UI.

## Validation targets

Test Python 3.9 (Blender 3.0), 3.10 (starting with Blender 3.1), and the actual
Python versions bundled with each supported newer Blender. Test Windows x64,
Linux x64, macOS Intel and macOS Apple Silicon where the Blender binary and wheel
both exist. Additional architectures require explicit wheel and Blender validation.
OS names alone are not compatibility promises: wheel minimum OS/glibc and CPU
requirements still apply. Missing binaries must fail the build, never compile or
download on a user's machine.

Tests must cover offline/read-only installation, registration and re-registration,
real Parquet I/O, both legacy and Extension namespaces, paths containing spaces,
failed/mismatched dependencies, and export dispatch. Full recording-to-animation
acceptance follows the Parquet loader work; do not label a packaging smoke test
as full export validation.

## Official guidance

- https://developer.blender.org/docs/handbook/extensions/addon_guidelines/
- https://docs.blender.org/manual/en/latest/advanced/extensions/python_wheels.html
- https://docs.blender.org/manual/en/latest/advanced/extensions/addons.html

Build tools may acquire pinned wheels. Runtime code must remain offline and must
not overwrite another add-on's loaded dependency or write into its installation.

## Build and test

Use a build-machine Python 3.9 or newer. No packages need to be installed into it.
The first build explicitly downloads pinned wheels from PyPI; subsequent builds
without `--download` require the cached lock and verify every wheel's SHA-256.
The lock is included in the resulting archive. Preserve the cache lock with
release artifacts for reproducibility. Acquisition trusts PyPI's HTTPS metadata;
hash checking is integrity verification, not an independent signature check.

```sh
# Blender 3.0 / Python 3.9, Windows example (runtime validation still required)
python -B tools/build_addon.py --kind legacy --python 3.9 --platform windows-x64 --download
# Blender 3.1 / Python 3.10: use --python 3.10 for the legacy package.
# A narrow Extension interval for the Blender version being tested:
python -B tools/build_addon.py --kind extension --python 3.11 --platform windows-x64 --blender-min 4.2.0 --blender-max 4.3.0 --download
python -B -m unittest discover -s tests -p test_dependency_packaging.py
python -B tools/test_blender_package.py --blender /path/to/blender --kind extension --archive dist/freemocap-extension-py3.11-windows-x64.zip
```

Other platform selectors are `linux-x64`, `macos-x64`, and `macos-arm64`.
Read the selected Blender's actual Python version before building. Manifest bounds
are an explicit maintainer responsibility; do not extend them across an ABI change.
Currently PyArrow 18.1.0 is selected for Python 3.9 and 25.0.1 for newer targets;
TOMLI 2.2.1 supplies TOML parsing where the standard library lacks it. NumPy comes
from Blender; do not replace it. Unsupported wheel targets fail during the build.

The smoke runner uses isolated test preferences and four separate Blender processes:
install, normal restart, disable after using the dependency, then restart and
re-enable. Logs and JSON reports stay under `.test-artifacts/`. The controlled
export-dispatch check writes a real empty Blender scene through a test writer;
it does **not** exercise recording reconstruction. Offline unit tests also run in
the new Windows/Linux/macOS CI workflow; that workflow does not certify Blender.

Install the resulting ZIP explicitly using Blender's install-from-disk UI. For
background export, use the saved configuration where that package is enabled:

```sh
blender --background --python-exit-code 1 --python tools/blender_export.py -- bl_ext.REPOSITORY.freemocap_blender_addon /recording /output/scene.blend
```

For legacy installations the package name is `freemocap_blender_addon`.
Select any required Rigify/Images as Planes capability explicitly in preferences;
FreeMoCap no longer enables other add-ons on the user's behalf. The existing
tag-release ZIP workflow has not been migrated to this builder: its source-only
archive is not a self-contained Parquet-capable distribution. Do not publish it
as one. Release automation migration follows validation of the supported matrix.

## Observed validation and limitations (2026-10-05)

- Nine offline unit tests pass locally on Windows/Python 3.12. They cover archive
  separation, repeatability, Python 3.9 parsing, relative imports, binary target
  rejection, traversal, hash tampering, and dependency conflict/failure behavior.
- Windows 11 x64, Blender 5.2.2 / Python 3.13.13: both package formats load
  PyArrow 25.0.1 and round-trip nullable Zstandard-compressed Parquet data offline.
- Both formats pass normal restart and re-enable after a process restart, including
  the controlled public export dispatch. A real
  failure was found when disabling and immediately re-enabling in the same
  process after importing PyArrow: Blender's wheel cleanup cannot remove loaded
  DLLs, and the next startup can lack required DLLs. **Restart Blender while the
  Extension is disabled, then re-enable it.** No add-on-side wheel repair, DLL
  deletion, or module eviction is attempted. This needs upstream Blender follow-up
  and testing on each supported release before general distribution.
- Blender 3.0/3.1/4.2 runtime coverage, macOS/Linux runtime coverage, read-only
  filesystem enforcement, full recording export, and official marketplace
  licensing/asset review remain outstanding. The official portable-binary server
  returned HTTP 403 in this environment; older-version tests were not executed.

## FreeMoCap integration handoff

After the human commits/pushes this add-on stage on `development-streaming`, core
must replace its environment-injection launcher with an installed-package call.
Core should discover/report Blender's version, Python ABI, architecture and exact
enabled package name; offer the matching package as an explicit installation
step; pass recording/output paths as arguments; and require nonzero exit status
on failure using `--python-exit-code 1`. It must not expose core's site-packages
to Blender, evict modules, or silently install the add-on during export.
Validate this integration independently before advancing to the three data loaders.
