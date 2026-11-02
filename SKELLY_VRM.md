# Skelly FreeMoCap VRM export

This offline tool creates VRM0 and VRM1 avatars from the established Forge
rest model and explicitly supplied, fitted Skelly artwork. VSeeFace currently
supports VRM0, not VRM1 [@vSeeFaceVrm0]. No Core or Forge installation is needed
inside Blender. The exporter is the official VRM Add-on for Blender [@vrmAddon4103].

| Target | Current artifact | File axes | Unity import |
| --- | --- | --- | --- |
| VRM0 (`--vrm-version 0.0`) | `Skelly.vrm` | right, up, backward | Reverse Z |
| VRM1 (`--vrm-version 1.0`) | `Skelly-vrm1.vrm` | left, up, forward | Reverse X |

These version-specific conventions follow UniVRM [@uniVrmCoordinateSystems;
@uniVrm0ImportAxis; @uniVrmImportAxisSettings; @uniVrm1ImportAxis]. Forge's existing
`vrm` convention explicitly means VRM1 and remains unchanged. The host preparer
uses Forge's public `CoordinateSystemConvention` and `CoordinateSystemTransform`
to derive the file, receiver and exporter-input transforms. It does not adjust
the scientific source or the VMC sender.

The original `Skelly.vrm` used VRM1-facing coordinates in a VRM0 file. The VRM0
import reflection then reversed the avatar's facing direction relative to the
sender, causing raised-arm rotations to move its artwork downward. The failing behavior is recorded in the regression evidence; the stable artifact
is replaced with the correction.

## What the avatar contains

The avatar retains all 61 source segments, the fitted surfaces of 55 rigid artwork
parts, 20,432 triangles, and the three existing material colors. It maps 21 body
joints and all 30 standard finger joints into the target humanoid vocabulary
[@vrm0Specification]. Thumb mappings use metacarpal/proximal phalanx/distal phalanx
as VRM0 proximal/intermediate/distal, or VRM1 metacarpal/proximal/distal. There is no added upperChest or substitute
scientific skeleton.

`prepare_skelly_vrm.py` reads Forge's public `SkeletonDefinition` and `RestPose`.
It rejects fitted artwork whose landmarks, parents or world rest orientations
differ from the current default model. The input retains the source hierarchy.
For the receiver rig, mapped joints use their nearest mapped ancestor: eight
non-thumb proximal finger bones become direct hand children, while their
metacarpal artwork bones remain hand children. This matches FreeMoCap's existing
VMC local-transform parent graph. It does not change scientific data, surface
geometry or world rest transforms. Standard VMC does not separately articulate
the extra metacarpal bones.

The current supplied artwork already includes the 0.90 skull adjustment and
thoracic shoulder-socket fit. The exporter does not apply them again. Authored
body-height units become meters using `--height-m` (default 1.75); a common
translation places the sole surface at ground level. This is a generic avatar
size, not a new estimate of the recorded person's height. Every vertex is bound
rigidly to its owning segment. The torso stays rigid; this export adds neither
soft-tissue deformation nor face expressions, eye tracking or jaw animation.

VRM0 starts with Forge's full rest roll; the official exporter freezes those
rotations into the skin binding. VRM1 uses the same world rest surfaces and joint
origins, with presentation bone axes prepared for identity exported transforms.
This cancels Blender glTF's bone-basis conversion rather than changing Forge's
rest pose [@blenderGltfJointExport]. Both deliverables have normalized nodes.
The VRM1 glTF exporter also eliminates one duplicate skull triangle, leaving
20,431 triangles with the same surface. This normalization is specific to these
Skelly artifacts; it does not establish compatibility for arbitrary VRM1 rigs.
For VSeeFace use the VRM0 file and FreeMoCap's `vrm0_normalized` VMC profile.

## Reproduce the artifact

Use an existing host Python with Forge, NumPy and SciPy installed. The separate
Blender process uses its bundled Python. Before creating outputs, verify the
owning repository ignores the output directory:

```text
git check-ignore .test-artifacts/vrm/Skelly.vrm
```

Obtain the official **4.10.3** legacy ZIP (`VRM_Addon_for_Blender-4_10_3.zip`)
from the release linked in `references.bib`. Verify SHA256
`dcf6d55f3d28de8c0de2f72abcc7fe06b2b300195e6b4da2e9cf476fd59165a2`.
Extract it under `.test-artifacts/vrm/extension`; the package directory is
`VRM_Addon_for_Blender-release`. The script loads it only in the background
process and never saves Blender preferences. Dependency acquisition is a
separate explicit setup action, not an automatic part of these scripts.

From this addon repository, substituting explicit executable/input paths:

```text
HOST_PYTHON tools/prepare_skelly_vrm.py --vrm-version 0.0 --artwork FITTED_SKELLY_JSON --height-m 1.75 --output .test-artifacts/vrm/avatar.json
BLENDER --background --factory-startup --python-exit-code 1 --python tools/export_skelly_vrm.py -- --input .test-artifacts/vrm/avatar.json --exporter .test-artifacts/vrm/extension/unpacked/VRM_Addon_for_Blender-release --output .test-artifacts/vrm/Skelly.vrm
HOST_PYTHON tools/validate_skelly_vrm.py --vrm .test-artifacts/vrm/Skelly.vrm --input .test-artifacts/vrm/avatar.json --build-report .test-artifacts/vrm/Skelly.build-report.json
```

For VRM1 select `--vrm-version 1.0` and separate input/output paths such as
`avatar-vrm1.json` and `Skelly-vrm1.vrm`.

### Fit the avatar to recorded proportions

The default `--height-m 1.75` export is a generic avatar. The native viewer
instead scales each artwork part using the current fitted segment length divided
by its authored length. A generic avatar therefore does not necessarily match
the viewer, even when their joint rotations agree.

Pass `--segment-scales-mm SEGMENT_SCALES_JSON` to the preparation command to use
the existing `ModelScaleFit.segment_scales` mapping in millimeters. Supply every
authored segment; missing, nonfinite or nonpositive values are rejected. This
overrides uniform fitting. For a recording that contains fitted `SEGMENT_LENGTHS`,
the equivalent mapping is each recorded fitted length divided by the matching
model's `length_proportion`. Do not substitute raw keypoint distances or mix
different model definitions. Record the selected frame/run and input provenance.

The preparer uses Forge's `build_rest_pose(segment_scales=...)` to calculate
attachments. Manifest version 3 retains the authored geometry and adds explicit
`fittedOriginMeters`, `fittedLengthMeters` and `artworkScaleMeters` per bone.
These fields, rather than the nominal `bodyHeightMeters`, control export geometry.
The source artwork and scientific skeleton are not modified.

This is a static fit snapshot. A receiver must also apply the transmitted bone
positions to reproduce changing reconstructed joint origins; rotation-only
playback cannot reproduce those translations. Standard VMC also omits separate
non-thumb metacarpal motion, so those palm pieces follow the hand. Neither
personalization nor the offline receiver simulation proves live surface contact.

The current fitted input is Core's
`freemocap-ui/src/components/viewport3d/renderers/skelly/skelly.json`, generated
from this addon's `assets/skelly_mesh.json.gz` and original
`assets/skelly_full_mesh_20k_faces.blend`. It is an explicit input file, not a
runtime package dependency. Its full hash is recorded in the build report.

Outputs are the selected `.vrm`, a diagnostic `.blend`, the build report and the
validation report. CPU checks exercise every mapped joint, invoke the official
validator, re-import the exported file, compare humanoid mappings and projected
hierarchy, and verify every weighted surface against the input, normalized node
transforms, meter-scale origins, inverse binds, triangle count and material colors.
`tools/check_skelly_vrm_receiver.py` additionally accepts decoded VMC fixtures,
imports the actual file-space skin/joints through the version's independent
receiver reflection, applies local messages, and compares all 55 artwork parts
with source poses. The current four cases cover T-pose, 45/90-degree arm raises,
asymmetric arms, body turn, root translation and an index curl. The original
file fails with about 0.316 m surface error; both corrected files pass below
0.3 micrometers. These CPU checks model published receiver semantics
[@vseeFacePreviewNodeImporter; @vseeFaceLocalReceiver], not the installed
proprietary application's entire Animator behavior or live acceptance.

```text
HOST_PYTHON -m unittest discover -s tools -p test_skelly_vrm_coordinates.py
HOST_PYTHON tools/check_skelly_vrm_receiver.py --vrm FILE.vrm --input INPUT.json --fixtures DECODED_VMC_FIXTURES.json --report .test-artifacts/vrm/receiver-report.json
```

## Receiver test

1. Add **`Skelly.vrm`** as a new local avatar in VSeeFace and load it, rather
   than reopening the cached original. VRM1 is for a separate compatible receiver.
   Confirm the skull,
   shoulders, fingers and feet look intact before starting motion.
2. Under VSeeFace's General settings, enable the VMC protocol receiver on port
   **39539**. Disable its local `Track ...` overrides during this test so they
   cannot replace received motion [@vSeeFaceVrm0].
3. In FreeMoCap's Streaming Outputs, start VMC for the intended human model and
   instance, with host **127.0.0.1**, port **39539**, profile
   **vrm0_normalized**, and **include_fingers** enabled. These are the current
   application defaults; select the intended source if more than one is active.
4. Using the existing running pipeline, compare Skelly in both applications:
   neutral stance, arms out, elbow bend, wrists turned, open hand, then a fist
   and thumb opposition on each side. Check left/right identity, shoulder
   attachment, finger direction and root movement.
5. Report whether loading, body movement and fingers pass separately. A sender's
   packet count alone does not establish receiver acceptance.

The owner policy allows everyone to use, modify and redistribute the avatar,
including commercial use, with attribution optional and no content restrictions.
The asset is provided under **CC0 1.0**, separately from the unchanged software
license. Credit to the FreeMoCap Foundation and free-of-charge availability of
Skelly-related assets to end users are appreciated, voluntary requests, not
license conditions. See [the asset notice](freemocap_blender_addon/assets/SKELLY_LICENSE.md)
and [machine-readable definition](freemocap_blender_addon/assets/skelly_asset.json).
The exporter embeds this notice and writes an adjacent `.LICENSE.txt`. VRM0
records CC0 directly. VRM1 retains its required VRM Public License URL and records
the separate CC0 offer; the additional URL is not presented as overriding the
format license. Export does not publish or upload the asset.

Filenames remain `Skelly.vrm` and `Skelly-vrm1.vrm`; the latter distinguishes the
format required by receivers, not an artifact revision. No numbered author
revision is embedded. VRM0/VRM1 specVersion values remain mandatory and correct.
