#!/usr/bin/env python3
"""Read-only design checks, adapted from nuyoah v0.2.1 under MIT.

Copyright (c) 2026 南鸢 nuyoah. See ../licenses/nuyoah-MIT.txt.
Changes: makeup components, bone-plan presence and portrait preference locks.
Checks encoded records only, never image quality or user authorization itself.
"""
import argparse
import itertools
import json
from pathlib import Path

AXES = {
    "face.ratio": ("short", "balanced", "long"),
    "face.midface": ("short", "balanced", "long"),
    "jaw.width": ("narrow", "medium", "wide"),
    "jaw.chin": ("round", "tapered", "square"),
    "eyes.length": ("short", "medium", "long"),
    "eyes.opening": ("small", "medium", "large"),
    "eyes.spacing": ("close", "medium", "wide"),
    "eyes.lid": ("single", "hooded", "double"),
    "eyes.tilt": ("down", "level", "up"),
    "nose.height": ("low", "medium", "high"),
    "nose.width": ("narrow", "medium", "wide"),
    "nose.tip": ("round", "defined", "broad"),
    "lips.width": ("narrow", "medium", "wide"),
    "lips.ratio": ("lower_fuller", "balanced", "upper_fuller"),
    "brows.arc": ("straight", "soft", "angled"),
    "brows.distance": ("close", "medium", "wide"),
}
GROUPS = ("face", "jaw", "eyes", "nose", "lips", "brows")
MAKEUP_KEYS = ("base", "eyes", "liner", "lashes", "blush", "lips")
BONE_KEYS = ("brow_socket", "cheek_transition", "jaw_chin", "soft_tissue")
PORTRAIT_LOCKS = {"head_roll_degrees": 0, "camera_roll_degrees": 0,
                  "gaze": "direct", "visible_text": False, "watermark": False}

def structural_difference(a, b):
    """Independent groups only; makeup, marks, skin and hair never add points."""
    changed = sorted({k.split(".")[0] for k in set(a) & set(b) if a[k] != b[k]})
    core = sorted(set(changed) & {"face", "eyes", "nose"})
    return changed, core

def check_workflow(workflow):
    """Check recorded stage prerequisites, not the truth of approval evidence."""
    if not isinstance(workflow, dict):
        return ["workflow must be an object"]
    errors = []
    def fail(message):
        errors.append("workflow: " + message)
    def nonempty(value):
        return isinstance(value, str) and bool(value.strip())
    stage = workflow.get("stage")
    stages = ("face-draft", "awaiting-face-approval", "awaiting-clothing", "ready-for-sheet", "sheet-delivered")
    if stage not in stages:
        fail("unknown stage")
    if workflow.get("final_product") != "character-reference-sheet":
        fail("final product must be character-reference-sheet")
    approved = workflow.get("face_approved")
    if type(approved) is not bool:
        fail("face_approved must be an explicit boolean")
    if stage in stages[1:] or approved is True:
        if not nonempty(workflow.get("face_image")):
            fail("selected face image required")
    if approved is True and not nonempty(workflow.get("face_approval_evidence")):
        fail("face approval evidence required")
    if stage == "awaiting-face-approval" and approved is True:
        fail("already approved face cannot still await approval")
    if stage in ("awaiting-clothing", "ready-for-sheet", "sheet-delivered") and approved is not True:
        fail("cannot advance without user face approval")
    clothing = workflow.get("clothing")
    if not isinstance(clothing, dict):
        fail("clothing must record pending, provided or none")
        clothing = {}
    mode = clothing.get("mode")
    refs = clothing.get("reference_images")
    if mode not in ("pending", "provided", "none"):
        fail("invalid clothing mode")
    if not isinstance(refs, list) or any(not nonempty(ref) for ref in refs):
        fail("clothing reference_images must be an array of paths")
    elif mode == "provided" and not refs:
        fail("provided clothing needs actual reference images")
    elif mode in ("pending", "none") and refs:
        fail("pending/none clothing must not claim reference images")
    if mode in ("provided", "none") and not nonempty(clothing.get("choice_evidence")):
        fail("explicit clothing choice evidence required; no attachment is not a none choice")
    if stage in ("ready-for-sheet", "sheet-delivered") and mode not in ("provided", "none"):
        fail("clothing choice required before sheet generation")
    if stage == "sheet-delivered" and not nonempty(workflow.get("sheet_image")):
        fail("actual final sheet path required")
    return errors

def unique_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON key: " + key)
        result[key] = value
    return result

def check(plan):
    errors, pairs = [], []
    def problem(message):
        errors.append(message)
    def axes_map(value, label, complete=False):
        if not isinstance(value, dict):
            problem(label + " must be an object")
            return {}
        for key, val in value.items():
            if key not in AXES:
                problem(label + ": unknown axis " + key)
            elif not isinstance(val, str) or val not in AXES[key]:
                problem(label + ": invalid value for " + key)
        if complete and set(value) != set(AXES):
            problem(label + ": complete canonical axes required")
        return {k: v for k, v in value.items()
                if k in AXES and isinstance(v, str) and v in AXES[k]}
    if not isinstance(plan, dict):
        return {"status": "FAIL", "errors": ["plan must be an object"], "pairs": []}
    if type(plan.get("schema_version")) is not int or plan["schema_version"] != 1:
        problem("schema_version must be 1")
    if "workflow" in plan:
        errors.extend(check_workflow(plan["workflow"]))
    req = plan.get("request")
    if not isinstance(req, dict):
        req = {}
        problem("request must be an object")
    if not isinstance(req.get("text"), str) or not req.get("text", "").strip():
        problem("request.text must retain the current request")
    if req.get("mode") not in ("text", "image"):
        problem("request.mode must be text or image")
    if type(req.get("explicit_image_request")) is not bool:
        problem("explicit_image_request must be a boolean")
    if req.get("mode") == "image" and req.get("explicit_image_request") is not True:
        problem("image mode lacks explicit current image request")
    goal = plan.get("roster_goal")
    if goal not in ("single", "distinct", "identity", "related"):
        problem("unknown roster_goal")
    same_makeup = plan.get("same_makeup", False)
    if type(same_makeup) is not bool:
        problem("same_makeup must be a boolean")
    locks = axes_map(plan.get("locks", {}), "locks")
    attribute_locks = plan.get("attribute_locks", {})
    if not isinstance(attribute_locks, dict):
        problem("attribute_locks must be an object")
        attribute_locks = {}
    require_bone = plan.get("require_bone_plan", goal in ("single", "distinct"))
    if type(require_bone) is not bool:
        problem("require_bone_plan must be a boolean")
    # Partial known references are allowed; do not invent unknown anatomy.
    reference = axes_map(plan.get("reference_axes", {}), "reference_axes")
    chars = plan.get("characters")
    if not isinstance(chars, list) or not chars:
        chars = []
        problem("characters must be a nonempty array")
    if goal == "distinct" and len(chars) < 2:
        problem("distinct requires at least two characters")
    if goal == "single" and len(chars) != 1:
        problem("single requires one character")
    ids, normalized, makeup_baseline = set(), [], None
    for index, char in enumerate(chars):
        label = "character[" + str(index) + "]"
        if not isinstance(char, dict):
            problem(label + " must be an object")
            continue
        ident = char.get("id")
        if not isinstance(ident, str) or not ident.strip() or ident in ids:
            problem(label + ": id must be unique and nonempty")
            ident = label
        ids.add(ident)
        axes = axes_map(char.get("axes"), ident + ".axes", goal == "distinct")
        attributes = char.get("attributes", {})
        if not isinstance(attributes, dict):
            problem(ident + ": attributes must be an object")
            attributes = {}
        for key, value in PORTRAIT_LOCKS.items():
            if key not in attributes or type(attributes[key]) is not type(value) or attributes[key] != value:
                problem(ident + ": portrait preference violation on " + key)
        for key, value in attribute_locks.items():
            if key not in attributes or attributes[key] != value:
                problem(ident + ": attribute lock violation on " + key)
        if require_bone is True:
            bone = char.get("bone_plan", {})
            if not isinstance(bone, dict) or any(not isinstance(bone.get(k), str) or not bone[k].strip() for k in BONE_KEYS):
                problem(ident + ": bone plan requires brow/socket, cheek, jaw/chin and soft-tissue descriptions")
        local_locks = axes_map(char.get("locks", {}), ident + ".locks")
        for key in set(locks) & set(local_locks):
            if locks[key] != local_locks[key]:
                problem(ident + ": local/global lock conflict on " + key)
        for key, value in {**locks, **local_locks}.items():
            if axes.get(key) != value:
                problem(ident + ": lock violation on " + key)
        if goal == "identity" and axes != reference:
            problem(ident + ": identity differs from reference_axes")
        if same_makeup is True:
            makeup = char.get("makeup")
            if (not isinstance(makeup, dict)
                    or any(not isinstance(makeup.get(k), str) or not makeup[k].strip()
                           for k in MAKEUP_KEYS)):
                problem(ident + ": complete makeup contract required")
            else:
                contract = {k: makeup[k] for k in MAKEUP_KEYS}
                if makeup_baseline is None:
                    makeup_baseline = contract
                elif contract != makeup_baseline:
                    problem(ident + ": makeup contract differs")
        normalized.append((ident, axes))
    if goal == "distinct":
        for (a_id, a), (b_id, b) in itertools.combinations(normalized, 2):
            changed, core = structural_difference(a, b)
            pairs.append({"a": a_id, "b": b_id, "groups": changed, "core": core})
            if len(changed) < 4 or len(core) < 2:
                problem(a_id + "/" + b_id + ": insufficient independent structural differences")
    return {"status": "FAIL" if errors else "PASS", "errors": errors, "pairs": pairs,
            "scope": "encoded constraints and field presence only; bone compatibility, prompt semantics and images require review"}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path)
    args = parser.parse_args()
    try:
        plan = json.loads(args.plan.read_text(encoding="utf-8"), object_pairs_hook=unique_keys)
        result = check(plan)
    except (OSError, UnicodeError, ValueError) as exc:
        result = {"status": "FAIL", "errors": ["Invalid input: " + str(exc)], "pairs": []}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
