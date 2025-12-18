# Wizard Blueprint

The `frontend/bootstrap/wizard_blueprint.py` file defines in one place:

- Which pages exist in the wizard (`nodes`)

- Which UI loads each page (`ui`)

- Which controller handles that UI (`controller`)

- How to navigate to the next node (`next`)

- How progress is calculated (`step`, `total_steps`)

- Where the flow starts (`start`)

## General Structure

Each node defines how the wizard decides the next node through the next field.

1) `type: "to"` — Static transition

    Always moves to a fixed target node.

    **Fields**

    - `type`: `"to"`

    - `target`: `str` (node id)

    **Example**

    ```json
    "next": {"type": "to", "target": "mode"}
    ```

    **Behavior**

    The next wizard that loads is the one for the “mode” key.

2) `type: "end"` — End of flow

    Indicates this is the last node in the wizard.

    **Fields**

    - `type`: `"end"`

    **Example**

    ```json
    "next": {"type": "end"}
    ```

    **Behavior**
    The dialog interpret as "finish"

3) `type: "switch"` — Conditional transition (routing)

    Routes based on a value stored in `WizardState`.

    **Fields**

    - `type`: `"switch"`

    - `cases`: `dict[str, str]` Mapping from state_value → node_id

    - `default`: `str` Node id to use when no case matches. If omitted, the result can be None.

    - `switch_on` (optional): `str` Attribute name in WizardState. default is "mode"

    **Example**
    ```json

    "next": {
        "type": "switch",
        "cases": {
            "basic": "basic_intro", 
            "advanced": "advanced_intro"
        },
        "default": "basic_intro",
        "switch_on": "mode"
    }
