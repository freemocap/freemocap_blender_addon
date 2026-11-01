# Blender addon agent guidance

This repository owns downstream Blender import, visualization, animation and
export. Reuse the recorded model and the owning components' public contracts;
keep upstream detector mappings and reconstruction algorithms with their owners.
Distinguish detector keypoints, mapped observations and reconstructed landmarks.

At milestones, checkpoint the task objective, decisions and reasons, exact
checkout, consumed recording products, existing interfaces, validation evidence
and next action. Include the relevant coordinate/rest-space assumptions and a
short recovery reading list. After compaction or handoff, read that checkpoint
and the relevant sources below, and inspect the current diff before editing:

- Recording ingestion: [Parquet reader](freemocap_blender_addon/freemocap_data_handler/parquet_recording.py).
- Scene and transform projection: [Parquet import](freemocap_blender_addon/core_functions/parquet_import.py)
  and [scene construction](freemocap_blender_addon/core_functions/parquet_scene.py).
- Route capabilities and provenance: [reconciliation](MAIN_RECONCILIATION.md).
- Validation and packaging: [TESTING.md](TESTING.md) and [DEPENDENCIES.md](DEPENDENCIES.md).

Verify which route and products the task concerns before changing transforms or
substituting data. Find existing conversions before implementing another one.
Resume authorized work once purpose, ownership and evidence are clear; ask only
for consequential intent that targeted inspection cannot resolve. Dated test
results are not current coverage. Preserve user data and edits, use ignored or
external test outputs, follow workspace policy when present, and leave Git state
to the human. Blender/dependency setup requires its own task authorization.
