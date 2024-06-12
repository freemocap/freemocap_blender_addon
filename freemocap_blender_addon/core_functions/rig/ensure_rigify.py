def ensure_rigify() -> None:
    _, rigify_enabled = addon_utils.check("rigify")

    if not rigify_enabled:
        try:
            print("Rigify not found - enabling Rigify addon...")
            addon_utils.enable(
                "rigify", default_set=True, persistent=True, handle_error=print
            )
        except Exception as e:
            print(f"Error enabling Rigify addon - \n\n{e}")
            raise e

    _, rigify_enabled = addon_utils.check("rigify")

    if not rigify_enabled:
        raise Exception(
            "Rigify not enabled, please enable it in your blender preferences and then close blender before retrying"
        )
