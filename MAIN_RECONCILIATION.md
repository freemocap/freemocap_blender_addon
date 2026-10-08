# Blender main reconciliation

Source: add-on main `549b0fd7fc840c8b0908a8373a986eca91c18ad8` (PRs 70, 71, 73, 74, 77).
Core main integration reference: `75c8acc2cd7fa486ee674021473be4b95b7be2cb`, especially PR 898.
The feature ports were committed as `d0dd5ef`. On 2026-10-08 the owner started
the Git merge of the source revision above. Conflict resolutions preserve those
reviewed ports and accept main's deletion of the unused `minimize_functions.py`
helper. The owner completes staging, the merge commit, and push.

## Incorporated behavior

- Nested configuration sections from main: `export_3d_model.formats`,
  `add_rig.rest_pose`, and `motion_cleanup` options. Legacy run-all uses them.
- T-pose/A-pose construction uses the same pose definition for rig and constraints.
  Standalone loading exposes this choice for legacy NPY and Parquet constraints.
- Revised foot-group locking, hand range-of-motion cleanup, and their UI controls.
- Missing optional hand-bone protections in mesh alignment, translation, rotation and scaling.
- Legacy timestamp-derived framerate, video texture frame offsets, plane facing and spacing.
- Layered action access adapted for Blender 4.4+ slots and older legacy actions.
- Python 3.9 compatibility, Extension-relative imports, bundled dependencies,
  canonical mesh attachment frames and original materials remain in place.

## Animation edits versus recorded data

The upstream cleanup algorithms edit Blender location F-curves. They do not write
NPY or Parquet recordings. Legacy run-all separately writes derived data before
its optional animation cleanup stage; that existing behavior is retained.

Parquet constraints have a separate set of legacy-named Blender animation targets.
Cleanup resolves those targets using explicit metadata; it never searches canonical
landmarks by a coincidental name. Imported landmarks, saved segment poses, COM and
source Parquet remain unchanged. COM continues to represent the recorded motion,
not the optionally cleaned Blender animation. Saving the .blend saves the edited
animation; it does not publish a new processing run.

Saved-segment skeletons are driven by supplied segment poses, not the legacy
constraint targets. Cleanup is explicitly rejected there until a segment-pose
animation editing method is implemented. No automatic route conversion occurs.

The legacy algorithms assume dense zero-based keyframes and the full recording
range. Other frame grids/ranges are rejected before editing rather than silently
renumbering frames. The hand range loop now includes the final frame. Legacy scene end is corrected
to N-1 for N zero-based samples, avoiding an extra frame and cleanup overrun.

## Supported export options

| Route | Model formats | Blender skeleton rest pose | Cleanup |
| --- | --- | --- | --- |
| legacy_npy | FBX, BVH (existing exporters) | T-pose, A-pose | Foot locking and hand limits |
| parquet_constraints | FBX | T-pose, A-pose | Foot locking and hand limits |
| parquet_segments | FBX | Preserve recorded model frames | Not supported |

`export_options.CAPABILITIES` exposes these differences to callers. For the
saved-segment route, the historical `tpose` option means the unchanged default;
it does not rotate measured segment poses into a new T-pose.

`export_api.export_recording(config=...)` accepts the nested JSON-compatible
configuration used by main. Parquet routes reject unsupported sections, options,
formats and rest poses before loading. Empty `formats` skips model sidecars.
Omitting Parquet configuration continues to save only the .blend; it does not
implicitly request main's legacy FBX+BVH defaults. The background helper accepts
`--config path/to/options.json`.

BVH for Parquet remains unimplemented. It requires a deliberate hierarchy/export
adapter, especially for independent saved segments; exposing main's default BVH
checkbox as supported would be misleading. Core should use these route capabilities
when reconciling its existing `BlenderExportConfig` and UI from main.

## Remaining integration work

### Deferred calibration/alignment workflow — 2026-10-07

The owner still sees camera/motion misalignment after reprocessing and suspects
person alignment is not consistently reflected in persisted calibration. Treat
this as an unresolved diagnosis, not a confirmed Blender transform bug. The
Blender audit verifies agreement with the saved extrinsics, not with image evidence.

Desired core workflow: a processing configuration choice to update/publish the
calibration with the calculated alignment, including person alignment and any
custom adjustment. Review the current "apply process transforms to calibration
file" action and its timing; a separate control-panel button is not the intended
workflow. Trace recording camera geometry separately from calibration-file
persistence, and guard against applying transforms twice. Validate projections
against observations when investigating. Do not compensate by rotating Blender
capture cameras. The owner explicitly deferred this work so core Blender-export
integration can proceed independently.

Core draft changes remain paused. After this add-on stage is reviewed, committed
and pushed by the owner, core can preserve main's export configuration while
switching installation/export transport to enabled, self-contained Blender packages.
Do not restore site-packages injection or silent dependency downloads.

This is feature reconciliation, not a claim that every legacy recording and
platform is validated. See TESTING.md for measured runtime coverage.
