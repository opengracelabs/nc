"""Product template validation."""


def verify_template_dimensions(asset_snapshot: dict, template: dict) -> dict:
    width = int(asset_snapshot.get("width_px") or 0)
    height = int(asset_snapshot.get("height_px") or 0)
    min_width = int(template.get("min_width_px") or 0)
    min_height = int(template.get("min_height_px") or 0)
    passed = width >= min_width and height >= min_height
    return {
        "passed": passed,
        "width_px": width,
        "height_px": height,
        "min_width_px": min_width,
        "min_height_px": min_height,
        "missing": [] if passed else ["minimum_image_dimensions"],
    }
