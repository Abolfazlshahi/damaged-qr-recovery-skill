# Using as an Agent Skill

## Minimal installation

Copy:

```text
skills/damaged-qr-recovery/
```

to the agent runtime's skill directory.

## Deeper execution

Keep the `references/` folder beside `SKILL.md`. The agent can load a reference when it reaches that part of the pipeline.

## Command entry points

- `commands/inspect.md` — evidence inventory.
- `commands/recover.md` — complete recovery.
- `commands/validate.md` — candidate proof.
- `commands/audit.md` — audit another recovery.

## Developer mode

```bash
python -m pip install -e '.[all]'
pytest
```
