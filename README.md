<p align="center">
    <img src="https://github.com/freemocap/freemocap/assets/15314521/da1af7fe-f808-43dc-8f59-c579715d6593" height="240" alt="Project Logo">
</p> 


<h3 align="center">FreeMoCap Blender Addon</h3>

Dependency packaging work and its current compatibility limits are documented in
[DEPENDENCIES.md](DEPENDENCIES.md). The new offline packages are under validation;
the existing release ZIP workflow does not yet use that builder.

[Testing](TESTING.md): run `python -B -m tools.run_tests` to test locally with
Blender Launcher builds and core's prepared test/sample datasets.



<p align="center">

<a href="https://doi.org/10.5281/zenodo.7233714">
    <img src="https://zenodo.org/badge/DOI/10.5281/zenodo.7233714.svg" alt=DOI-via-Zenodo.org>
  </a>

<a href="https://github.com/psf/black">
    <img alt="https://img.shields.io/badge/code%20style-black-000000.svg" src="https://img.shields.io/badge/code%20style-black-000000.svg">
  </a>

<a href="https://github.com/freemocap/freemocap_blender_addon/releases/latest">
        <img src="https://img.shields.io/github/release/freemocap/freemocap_blender_addon.svg" alt="Latest Release">
    </a>

<a href="https://github.com/freemocap/freemocap/blob/main/LICENSE">
        <img src="https://img.shields.io/badge/license-AGPL-blue.svg" alt="AGPLv3">
    </a>

<a href="https://github.com/freemocap/freemocap/issues">
        <img src="https://img.shields.io/badge/contributions-welcome-ff69b4.svg" alt="Contributions Welcome">
    </a>

<a href="https://github.com/psf/black">
    <img alt="https://img.shields.io/badge/code%20style-black-000000.svg" src="https://img.shields.io/badge/code%20style-black-000000.svg">
  </a>

<a href="https://discord.gg/SgdnzbHDTG">
    <img alt="Discord Community Server" src="https://dcbadge.vercel.app/api/server/SgdnzbHDTG?style=flat">
  </a>


</p>

This is a Blender add-on for loading and visualizing the output of the [freemocap](https://freemocap.org) software. 

The core functionality is run automatically at the end of a standard freemocap recording session, but this add-on allows for manual loading and visualization of the pre-processed `freemocap` recording data in Blender.

![image](https://github.com/freemocap/freemocap_blender_addon/assets/15314521/94d482c1-9fa7-4c66-8354-34cf5707af9f)

# Installation

For source development with JacquesLucke's VS Code extension, first prepare the
dependency-equipped workspace using the [development setup](DEPENDENCIES.md#vs-code-development).
Opening the raw source folder alone does not provide PyArrow to Blender.

1. Download the `freemocap_blender_addon.zip` ([from the latest release](https://github.com/freemocap/freemocap_blender_addon/releases/latest))
1. Open [Blender]()
1. `Edit` > `Preferences` > `Add-ons` > `Install...` 
1. Select the `freemocap_blender_addon.zip` (likely from your `Downloads/` folder) 
1. Verify installation by searching `freemocap` in the addon tab and ensuring the box next to `freemocap_blender_addon` is checked

## Usage
> NOTE - *We strongly recommend activating your System Console before running this addon, as it will show oodles of valuable information about the underlying process. On Windows, you can toggle this console on from the `Window` menu in a running instance of Blender. On Mac/Linux, you must **launch** blender from a Terminal by typing `blender` into a terminal after install.*

### Pre-requisites - Data!
You must have should have a fully processed [freemocap](https://freemocap.org) recording folder on your computer somewhere. 

If you are processing a recording from the `freemocap` software, it will probably in in `[path_to_your_home_directory]/freemocap_data/recording_sessions/[recording_name]`

If you have downloaded and processed the `test` data from the `Data` dropdown in the menu bar of the `freemoap` software, the addon should detect that automatically and set that path as the default.

You may download a pre-processed `freemocap_test_data` recording on the [`freemocap==1.3.0` release notes](https://github.com/freemocap/freemocap/releases/download/v1.3.0/):
> https://github.com/freemocap/freemocap/releases/download/v1.3.0/freemocap_test_data_processed_with_freemocap_v1.3.0.zip
    

## Running the skeleton building pipeline

### Current Parquet recordings

In the **💀FreeMoCap → Load FreeMoCap Data** panel, choose the recording folder
containing `*_data.parquet`, then select an **Import route**:

| Route | Input | Blender result |
| --- | --- | --- |
| Parquet: saved segments | `LANDMARKS_3D`, `SEGMENT_ORIGINS`, `ROTATIONS_WORLD` | Canonically named landmarks, segment axes, and a **Blender skeleton** displaying the saved independent world poses |
| Parquet: legacy constraints | `LANDMARKS_3D` by default; optionally `MAPPED_KEYPOINTS_3D` | Canonical trajectories plus an explicit compatibility projection into the existing connected Blender armature and tracking constraints |
| Legacy NPY recording | Original recording folder | Existing loading and processing pipeline |

**Load Data** adds a Parquet import to the current scene without clearing it or
writing into the recording. Load both routes to compare them, then save the scene
normally. Select a run explicitly or leave `-1` to use the file's selected run.
Leave sensor group blank only when there is a single matching group.

The native route selects `model:standard_human`; it never selects optional
`skeleton_fit:*` results. Tracker keypoints, mapped keypoint observations, model
landmarks, and the Blender skeleton are distinct concepts. No tracker package or
SkellyForge installation is needed inside Blender: the model snapshot is in the
Parquet metadata. Millimeters become meters; world wxyz rotations retain their
Blender coordinate basis. Source frame numbers and timestamps are retained;
playback uses the median sample rate. Contiguous, nonnegative frame numbers are
required. Animation holds each measured sample until the next frame.

Native segment bones are deliberately independent, with anatomical parents saved
as metadata. Connecting them would change the saved poses and could hide valid
children when a parent is missing. Missing native samples are hidden/collapsed
and carry an animated `sample_valid` property. Bone drawing axes have a fixed
conversion to Blender's local bone Y axis; segment objects carry the exact saved
world quaternion. Model scales determine the bone display lengths.

The comparison route reuses the old armature, median bone lengths, and Blender
tracking constraints. It keeps canonical centers and projects names only at the
constraint-target boundary (`pelvis_origin` → `hips_center`, `chest_center` →
`trunk_center`, canonical digits → old hand names). Its hand-midpoint helper uses
the old index/pinky tip average. Legacy targets retain the old missing-data
hold/backfill behavior; the separate canonical trajectories retain validity.
This route does not rerun the old preprocessing/landmark adjustment pipeline.
The two skeletons need not be numerically identical.

Both Parquet routes also build the Skelly mesh, rigid segment meshes, saved
center of mass (when present), video planes, capture cameras, ground, lighting,
and an overview camera. **Data View Settings → Scope data parent** selects an
import; its visibility controls switch the armature, landmarks, rigid bodies,
Skelly mesh, videos, and center of mass. Both mesh layers and the COM sphere start visible, as in the run-all controller;
landmark axes start hidden. These presentation objects do not
alter the native saved segment poses.

The portable Skelly artwork uses the same +X right, +Y forward, +Z up convention
as the recorded model. Each part declares a rest-world roll reference in addition
to its origin and endpoint: endpoint alignment alone cannot orient a skull or
pelvis. The skull, pelvis, and thorax attach using their model-defined secondary
landmarks. Parts without that definition use the model's parent-relative rest
rotations and the asset's roll reference to map into segment local space. The loader applies the
saved world poses unchanged. The legacy attachment boundary converts the artwork
back to its historical basis. The editable `.blend` remains the source artwork;
`tools/extract_skelly_asset.py` reproduces the canonical portable asset.

Both Parquet routes use the existing cone-and-joint stick mesh builder and its
left/right/hand palette. The anatomical Skelly layer retains the source asset's
Base, Cavities, and Sparkles materials and per-face assignments. The COM sphere
uses the existing cyan/magenta checkerboard builder; the shared ground builder
uses the run-all controller's dark navy checks (0.5 m squares). The Sparkles
material belongs to the anatomical asset. COM trails remain an optional
controller operation outside the run-all sequence.

Videos come from `annotated_videos`, falling back to `synchronized_videos` beside
the Parquet. Keep those folders beside it when moving a recording. The `.blend`
references the movies; it does not embed them. Camera geometry comes from the
selected run/sensor group in the Parquet, and camera backgrounds match video
filenames to camera IDs. No Images as Planes extension is required for these
routes. The completion message reports actual video and camera counts, including
zero when those resources are absent. Blender cameras use the pinhole intrinsics;
recorded lens distortion remains metadata, not a distortion compositor.

The existing **Export 3D Model** panel supports Parquet **FBX** export using
default names/rest pose, without changing trajectory keyframes. Other export
formats and legacy rest-pose/renaming conversions are explicitly rejected for
Parquet scenes. Legacy editing/analysis tools such as foot locking and custom
joint overlays are not part of this scene-loading acceptance and should not be
assumed to support canonical names. The original NPY route remains available.

For headless callers, the installed package exposes:

```python
from freemocap_blender_addon.export_api import export_recording

export_recording(
    recording_path="C:/recordings/session/session_data.parquet",
    blend_file_path="C:/exports/session.blend",
    route="parquet_segments",  # or "parquet_constraints"
)
```

For an Extension, import through its installed `bl_ext.<repository>.<package>`
namespace. The API default remains `legacy_npy` for existing callers. Parquet
routes reject a legacy processing `config` instead of silently ignoring it.
FreeMoCap core must opt into the new route in a separate integration change.

Both Parquet routes support FBX and BVH through Blender's exporters, from the
Export 3D Model panel or `config={"export_3d_model": {"formats": ["fbx", "bvh"]}}`
in the export API. BVH exports the loaded armature and does not require a Skelly
mesh. It evaluates the scene frame range with non-root translations enabled,
matching the legacy Blender BVH settings. Bone names and the current rest pose
are preserved. Deferral of a standalone FreeMoCap FBX/BVH writer does not restrict
these Blender exports.

Saved-segment missing samples use zero scale for display, which BVH cannot encode.
BVH export uses a temporary copy with unit scale, retaining the loader's existing
zero-location/identity-rotation placeholders at those samples. A neighboring
`.bvh.metadata.json` records missing frame numbers by bone. The original scene,
animation and sample validity are unchanged; BVH alone does not preserve visibility.

Core integration handoff: after this add-on change is committed and pushed on
`development-streaming`, update core's consumed add-on revision and remove its
legacy-only BVH checks in `BlenderExportConfig`, `BlenderPackageSettings`, and
`blender-slice`. Verify that changing Parquet routes retains BVH selection and
that automatic and manual export requests reach Blender. Those core changes
are a separate repository stage; add-on support alone does not enable the core UI.

### Local acceptance tests

Run from the add-on repository with its existing Python environment:

```powershell
.venv/Scripts/python.exe -B -m tools.run_tests
```

The runner discovers Blender Launcher installations and tests every discovered
build using legacy ZIPs plus Extensions where
supported. It snapshots core's accepted prepared test/sample recordings, verifies
their provenance, and checks that the shared originals remain unchanged. Use
`--blender "C:/path/to/blender.exe"` to select a build, or `--dataset test_data`
for a smaller run. Reports and saved `*-both-routes.blend` comparison scenes are
under `.test-artifacts/suite-*/build-*/<install-kind>/`.

Tests verify all native landmark and segment samples, actual legacy constraint
targets and responses, numerical limb-origin differences, saved-scene reloads,
and the public export API.
BVH exports from both Parquet routes are reimported and checked for hierarchy,
frame count, frame time, and sampled bone positions/rotations. Anatomical attachment checks independently verify
skull up/forward and pelvis left/right, including the antiparallel frame case;
both routes must preserve the separate stick, authored Skelly, COM, and ground
materials and visibility defaults.
Small adversarial fixtures reject ambiguous selection,
duplicate/missing components, conflicting timestamps, wrong units/basis, and
non-unit rotations; they also check that a missing parent does not remove a valid
child. The older NPY API dispatch remains covered separately. Full legacy NPY
recording processing still requires an old-format recording fixture.

### Original NPY workflow

1. In the `3D viewport` window, press `n` to show the sidebar
2. Select the `💀FreeMoCap` tab
3. Set the path to the FreeMoCap recording you want to load (path should point to the directory that contains the `output_data/` and `annotated_videos/` folders)
4. Press the `RUN_ALL` (keep an eye on the terminal window for useful output) 

# 💀✨ Time for skeletons \o/ 
If all went well, there should now be a friendly spooky skeleton in your scene along with the annotated images-as-planes, and a new `.blend` file saved to the specified recording folder named `[recording_folder_name].blend` (i.e. the same way it comes out of a standard `freemocap` recording session) 


___
# Considerations:

- The rig has a TPose as rest pose for easier retargeting.
- For best results, your recording should include a few seconds where the particapant is standing still with their feet clearly visible flat on the ground.
- If the data comes out rotated relative to gravity, it can be globally manipulated using the parent `empty`
 object (usually named `[recording_name]_parent_empty`) in the scene.
- This is a Work-In-Progress with significant refactors/overhauls planned for the near future. You will always be able to re-process old freemocap recordings using new versions of software, but things like naming conventions, armature configuration, etc may change without notice! Save your work often and back up your data often :D 

# Special Thanks
 Special thanks to @ajc27-git for the original work developing this addon and supporting the `freemocap` community! Check out their work at:  https://www.youtube.com/@fluxrenders
 
# Join the FreeMoCap Discord Community for support, feedback, and collaboration!
Click this link to join the our community Discord server - https://discord.gg/XpRQJnqZxf


Main-branch feature reconciliation and route-specific export capabilities are documented in [MAIN_RECONCILIATION.md](MAIN_RECONCILIATION.md).
