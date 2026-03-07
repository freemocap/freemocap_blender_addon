import bpy
from pathlib import Path
from ajc27_freemocap_blender_addon import PACKAGE_ROOT_PATH


def add_gaze_visuals(
    data_parent_name: str,
    driver_multiplier: float = 0.5
):
    """
    Appends pre-built gaze visual meshes from .blend files and applies the
    appropriate constraints and drivers to each one.

    For each eye it appends:
      - FOV_Limit_{side}:  copy location (eye empty) + copy rotation (face bone).
                           No drivers – represents the anatomical field-of-view limit.
      - FOV_Gaze_{side}:   copy location (eye empty) + copy rotation (face bone)
                           + eye-rotation drivers, representing the live gaze direction.

    Blend file paths (assets/gaze_visuals/):
      FOV_Gaze_Left.blend
      FOV_Gaze_Right.blend
      FOV_Limit_Left.blend
      FOV_Limit_Right.blend
    """
    if data_parent_name not in bpy.data.objects:
        print(f"Warning: data_parent '{data_parent_name}' not found!")
        return

    data_parent = bpy.data.objects[data_parent_name]

    # ── 1. Find required scene objects ───────────────────────────────────────
    right_eye_empty = None
    left_eye_empty = None
    armature = None
    arkit_blendshapes = None

    for child in data_parent.children_recursive:
        if "right_eye" in child.name:
            right_eye_empty = child
        elif "left_eye" in child.name:
            left_eye_empty = child
        elif "arkit_face_blendshapes" in child.name:
            arkit_blendshapes = child
        elif child.type == 'ARMATURE':
            armature = child

    if not right_eye_empty or not left_eye_empty or not armature:
        print("Warning: Missing required objects (right_eye, left_eye, or armature).")
        return

    # ── 2. Create gaze_visuals empty parent ───────────────────────
    bpy.ops.object.select_all(action='DESELECT')

    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
    gaze_visuals_empty = bpy.context.active_object
    gaze_visuals_empty.name = "gaze_visuals"
    gaze_visuals_empty.parent = data_parent
    gaze_visuals_empty.hide_set(True)

    # ── 3. Asset paths ────────────────────────────────────────────────────────
    gaze_visuals_dir = Path(PACKAGE_ROOT_PATH) / "assets" / "gaze_visuals"

    asset_paths = {
        "FOV_Gaze_Left":   str(gaze_visuals_dir / "FOV_Gaze_Left.blend"),
        "FOV_Gaze_Right":  str(gaze_visuals_dir / "FOV_Gaze_Right.blend"),
        "FOV_Limit_Left":  str(gaze_visuals_dir / "FOV_Limit_Left.blend"),
        "FOV_Limit_Right": str(gaze_visuals_dir / "FOV_Limit_Right.blend"),
    }

    # ── 4. Per-eye info ───────────────────────────────────────────────────────
    eyes_info = [
        {
            "side": "Right",
            "target": right_eye_empty,
            "objects": [
                {"blend_key": "FOV_Limit_Right", "use_drivers": False},
                {"blend_key": "FOV_Gaze_Right",  "use_drivers": True},
            ],
        },
        {
            "side": "Left",
            "target": left_eye_empty,
            "objects": [
                {"blend_key": "FOV_Limit_Left", "use_drivers": False},
                {"blend_key": "FOV_Gaze_Left",  "use_drivers": True},
            ],
        },
    ]

    # ── 5. Process each mesh ──────────────────────────────────────────────────
    # Keeps track of appended objects by blend_key so FOV_Gaze can reference
    # the already-appended FOV_Limit object for the Boolean modifier.
    appended_objects: dict = {}
    for info in eyes_info:
        side   = info["side"]
        target = info["target"]

        for obj_info in info["objects"]:
            blend_key  = obj_info["blend_key"]   # e.g. "FOV_Gaze_Right"
            blend_path = asset_paths[blend_key]
            use_drivers = obj_info["use_drivers"]

            # ── Append from .blend ────────────────────────────────────────
            # We always append a fresh copy; Blender will auto-suffix the name
            # (e.g. FOV_Gaze_Right.001) when multiple captures are loaded in the
            # same session – that's fine, we grab whichever object was just linked.
            appended_obj = None
            with bpy.data.libraries.load(blend_path, link=False) as (data_from, data_to):
                if blend_key in data_from.objects:
                    data_to.objects.append(blend_key)

            # Link the freshly appended object (parent is None = not yet in any scene)
            for obj in bpy.data.objects:
                if blend_key in obj.name and obj.parent is None:
                    bpy.context.collection.objects.link(obj)
                    appended_obj = obj
                    break

            if appended_obj is None:
                print(f"Warning: Could not append '{blend_key}' from {blend_path}")
                continue

            # ── Parent to gaze_visuals empty ──────────────────────────────
            appended_obj.parent = gaze_visuals_empty
            appended_obj.rotation_mode = 'XYZ'

            # ── Constraint 1: Copy Location → eye empty ───────────────────
            loc_con = appended_obj.constraints.new(type='COPY_LOCATION')
            loc_con.target = target

            # ── Constraint 2: Copy Rotation → face bone ───────────────────
            rot_con = appended_obj.constraints.new(type='COPY_ROTATION')
            rot_con.target      = armature
            rot_con.subtarget   = "face"
            rot_con.mix_mode    = 'ADD'
            rot_con.target_space = 'WORLD'
            rot_con.owner_space  = 'WORLD'

            # ── Drivers (FOV_Gaze only) ───────────────────────────────────
            if use_drivers and arkit_blendshapes:

                # Driver X – Eye Pitch (look up / down)
                driver_x = appended_obj.driver_add("rotation_euler", 0)

                var_up = driver_x.driver.variables.new()
                var_up.name = "look_up"
                var_up.type = 'SINGLE_PROP'
                var_up.targets[0].id = arkit_blendshapes
                var_up.targets[0].data_path = f'["eyeLookUp{side}"]'

                var_down = driver_x.driver.variables.new()
                var_down.name = "look_down"
                var_down.type = 'SINGLE_PROP'
                var_down.targets[0].id = arkit_blendshapes
                var_down.targets[0].data_path = f'["eyeLookDown{side}"]'

                driver_x.driver.expression = (
                    f"(look_down - look_up) * {driver_multiplier}"
                )

                # Driver Z – Eye Yaw (look in / out)
                driver_z = appended_obj.driver_add("rotation_euler", 2)

                var_in = driver_z.driver.variables.new()
                var_in.name = "look_in"
                var_in.type = 'SINGLE_PROP'
                var_in.targets[0].id = arkit_blendshapes
                var_in.targets[0].data_path = f'["eyeLookIn{side}"]'

                var_out = driver_z.driver.variables.new()
                var_out.name = "look_out"
                var_out.type = 'SINGLE_PROP'
                var_out.targets[0].id = arkit_blendshapes
                var_out.targets[0].data_path = f'["eyeLookOut{side}"]'

                if side == "Right":
                    driver_z.driver.expression = (
                        f"(look_in - look_out) * {driver_multiplier}"
                    )
                else:
                    driver_z.driver.expression = (
                        f"(look_out - look_in) * {driver_multiplier}"
                    )

            # ── Boolean modifier (FOV_Gaze only) ─────────────────────────────
            # NOTE: We disable show_viewport / show_render BEFORE assigning
            # bool_mod.object to prevent Blender from immediately triggering a
            # depsgraph evaluation.  At setup time both meshes share identical
            # world transforms (both copy the same eye empty), which makes the
            # Exact solver's intersection degenerate and causes an infinite hang.
            # The flags are restored to True after all objects are fully built.
            # if use_drivers:  # use_drivers == True means this is an FOV_Gaze mesh
            #     limit_key = blend_key.replace("FOV_Gaze", "FOV_Limit")  # e.g. "FOV_Limit_Right"
            #     limit_obj = appended_objects.get(limit_key)
            #     if limit_obj is not None:
            #         bool_mod = appended_obj.modifiers.new(
            #             name="Boolean_FOV_Limit", type='BOOLEAN'
            #         )
            #         bool_mod.operation    = 'INTERSECT'
            #         bool_mod.solver       = 'EXACT'
            #         # Disable before assigning object to suppress eager DG eval
            #         bool_mod.show_viewport = False
            #         bool_mod.show_render   = False
            #         bool_mod.object        = limit_obj
            #         # Re-enable immediately; DG won't re-evaluate until next update
            #         bool_mod.show_viewport = True
            #         bool_mod.show_render   = True
            #     else:
            #         print(
            #             f"Warning: Could not find '{limit_key}' to use as "
            #             f"Boolean target for '{blend_key}'."
            #         )

            # ── Store reference for later use (e.g. Boolean target) ───────────
            appended_objects[blend_key] = appended_obj
