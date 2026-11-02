# Skelly VRM export

This offline tool creates a VRM0 avatar for VSeeFace from the established Forge
rest model and explicitly supplied, fitted Skelly artwork. VSeeFace currently
supports VRM0, not VRM1 [@vSeeFaceVrm0]. No Core or Forge installation is needed
inside Blender. The exporter is the official VRM Add-on for Blender [@vrmAddon4103].

## What the avatar contains

The avatar retains all 61 source segments, the fitted surfaces of 55 rigid artwork
parts, 20,432 triangles, and the three existing material colors. It maps 21 body
joints and all 30 standard finger joints into the VRM0 humanoid vocabulary
[@vrm0Specification]. Thumb mappings use metacarpal/proximal phalanx/distal phalanx
as VRM0 proximal/intermediate/distal. There is no added upperChest or substitute
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

Blender bone +Y represents Forge's local +Z with the full rest roll retained.
The official exporter performs VRM0 axis conversion and normalizes node rotations
and scales [@vrmAddon4103]. Use FreeMoCap's `vrm0_normalized` VMC profile.

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
HOST_PYTHON tools/prepare_skelly_vrm.py --artwork FITTED_SKELLY_JSON --height-m 1.75 --output .test-artifacts/vrm/avatar.json
BLENDER --background --factory-startup --python-exit-code 1 --python tools/export_skelly_vrm.py -- --input .test-artifacts/vrm/avatar.json --exporter .test-artifacts/vrm/extension/unpacked/VRM_Addon_for_Blender-release --output .test-artifacts/vrm/Skelly.vrm
HOST_PYTHON tools/validate_skelly_vrm.py --vrm .test-artifacts/vrm/Skelly.vrm --input .test-artifacts/vrm/avatar.json --build-report .test-artifacts/vrm/Skelly.build-report.json
```

The current fitted input is Core's
`freemocap-ui/src/components/viewport3d/renderers/skelly/skelly.json`, generated
from this addon's `assets/skelly_mesh.json.gz` and original
`assets/skelly_full_mesh_20k_faces.blend`. It is an explicit input file, not a
runtime package dependency. Its full hash is recorded in the build report.

Outputs are `Skelly.vrm`, a diagnostic `Skelly.blend`, the build report and the
validation report. CPU checks exercise every mapped joint, invoke the official
validator, re-import the exported file, compare humanoid mappings and projected
hierarchy, and verify every weighted surface against the input, normalized node
transforms, meter-scale origins, inverse binds, triangle count and material colors.
These checks do not certify VSeeFace's runtime behavior.

## Receiver test

1. Add `Skelly.vrm` as a local avatar in VSeeFace and load it. Confirm the skull,
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

The initial artifact is for local review. Existing repository guidance leaves
asset-specific licensing/provenance review open. Metadata is deliberately
restrictive pending that review; it does not replace or grant rights in the
source artwork. Do not interpret successful export as a publication decision.
