"""NC-COMMERCE-002 product activation state machine."""

TRANSITIONS = {
    "draft": {"verify": "ready"},
    "ready": {"package": "packaged", "retract": "retracted"},
    "packaged": {"activate": "activated", "retract": "retracted"},
    "activated": {"pause": "paused", "retract": "retracted"},
    "paused": {"resume": "activated", "retract": "retracted"},
    "retracted": {},
}


def transition_activation_state(current_state: str, action: str) -> str:
    allowed = TRANSITIONS.get(current_state, {})
    if action not in allowed:
        raise ValueError(
            f"Cannot apply action '{action}' from activation state '{current_state}'"
        )
    return allowed[action]


def activation_actions(current_state: str) -> list[str]:
    return sorted(TRANSITIONS.get(current_state, {}))
