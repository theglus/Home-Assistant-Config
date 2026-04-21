# Home Assistant Configuration

This is a personal Home Assistant configuration repository for a heavily customized smart home setup. It is not an application codebase — there is no build step, no tests to run, and no deployment pipeline. Changes are applied by validating via the HA UI config check, then restarting Home Assistant.

**Always read `README.md` at the start of every session.** It describes the physical smart home setup (devices, areas, integrations) and how it maps to the codebase. This context is essential for understanding the config.

## Collaboration Style

Act as a collaborative partner, not just a code generator. The ongoing goals are:
- Expanding automations and integrations
- Refactoring and cleaning up existing config

The user will provide questions describing what they need. Ask follow-up questions before making changes if the scope or intent is unclear.

## Structure

- `configuration.yaml` — root config, uses `!include` and `!include_dir_*` to split files
- `integrations/` — one file per HA domain; each contains a domain key and an `!include` or `!include_dir_*` pointing into `includes/`. This directory is loaded as packages via `homeassistant.packages: !include_dir_named integrations` in `configuration.yaml`.
- `includes/` — split YAML files for automations, scripts, sensors, templates, etc.
- `blueprints/` — blueprint YAML files

## Validation

Config is validated using the **Check Configuration** button in the Home Assistant UI (Developer Tools → YAML → Check Configuration). There is no CLI or automated check — always remind the user to run this after making changes.

## Languages & Formats

- YAML for all configuration
- Jinja2 templates used heavily in automations, templates, and scripts
- No JSON configuration files

## Rules

- **NEVER edit `secrets.yaml`** under any circumstances
- **Always warn before deleting** any file or config block — ask for confirmation first
- Keep comments minimal; only add comments to explain non-obvious Jinja2 logic
- When editing split files, preserve the existing `!include` reference structure — do not inline content back into `configuration.yaml`
- Do not modify automations or scripts the user has not explicitly asked about

## Conventions

- Follow existing `!include` and `!include_dir_merge_list` patterns when adding new split files
- Place new integration configs in `includes/` and reference them from `integrations/`
- Match the naming style of existing entities in the repo (e.g. `sensor.living_room_temp`)
- When writing Jinja2 templates, prefer readability and test edge cases (unavailable states, None values)
- `automations.yaml`, `scripts.yaml`, and `scenes.yaml` at the repo root are GUI-generated — they use numeric timestamp IDs and should not be edited manually. New automations, scripts, and scenes belong in `includes/automations/`, `includes/scripts/`, and `includes/scenes/` respectively, using UUID-style IDs.
- When adding a new automation or script, identify the appropriate thematic sub-folder under `includes/automations/` or `includes/scripts/` (e.g. `climate/`, `notify/`, `shutoff/`, `vacuum/`, `leave/`, `dimmer/`, `m5stack/`) and confirm with the user before creating the file.
