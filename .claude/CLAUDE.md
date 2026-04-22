# Home Assistant Configuration

This is a personal Home Assistant configuration repository for a heavily customized smart home setup. It is not an application codebase — there is no build step, no tests to run, and no deployment pipeline. Changes are applied by validating via the HA UI config check, then restarting Home Assistant.

## Home Layout

- **Rooms:** Entryway, Office, Living Room, Kitchen, Loft
- **Named devices:** Winston (Roborock S4 vacuum), Kirby (Dyson TP04 fan/purifier, loft), Ice Bear (Frigidaire portable AC, living room)
- **Lighting:** Primarily Philips Hue via the Hue bridge — not ZHA. Non-Hue devices (Sengled LED strip, Sengled plugs) are on ZHA.
- **Presence:** Aqara Mini Switch at the front door (single/double/long press), not motion sensors
- **Hardware:** Raspberry Pi 4 (4GB) + Home Assistant Connect ZBT-1 Zigbee coordinator

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
- `esphome/` — ESPHome device configs (M5Stack Atom Echo wake word devices, Bluetooth proxies); use `!secret` for API keys and WiFi credentials

## Context Files

Pre-built context files live in `.claude/context/`. Load them when relevant rather than exploring the codebase.

- `integrations-list.md` — Load when writing automations, scripts, or templates to understand what integrations and services are available.
- `integrations-reference.md` — Load on-demand when looking up integration options or services. Pass relevant URLs directly to the ha-researcher agent rather than searching from scratch.
- `lovelace-reference.md` — Load on-demand for UI layout work. Contains dashboard screenshots by room.

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

- Use the correct `!include_dir_*` variant when adding new split files:
  - `!include_dir_list` — for automations, scenes, lights, notifiers (produces a list of items)
  - `!include_dir_merge_list` — for sensors, templates, powercalc (merges files into a single flat list)
  - `!include_dir_merge_named` — for scripts (merges files into a single dict, preserving script name keys)
- Place new integration configs in `includes/` and reference them from `integrations/`
- Match the naming style of existing entities in the repo — device-name-based (e.g. `sensor.kirby_temperature`, `vacuum.winston`) or descriptive (e.g. `switch.major_laser_printer`, `fan.air_circulator`)
- When writing Jinja2 templates, prefer readability and test edge cases (unavailable states, None values)
- `automations.yaml`, `scripts.yaml`, and `scenes.yaml` at the repo root are GUI-generated — they use numeric timestamp IDs and should not be edited manually. New automations, scripts, and scenes belong in `includes/automations/`, `includes/scripts/`, and `includes/scenes/` respectively, using UUID-style IDs.
- When adding a new automation or script, identify the appropriate thematic sub-folder under `includes/automations/` or `includes/scripts/` (e.g. `climate/`, `notify/`, `shutoff/`, `vacuum/`, `leave/`, `dimmer/`, `m5stack/`) and confirm with the user before creating the file.
- Every split file must begin with the standard header comment block:
  ```yaml
  #################################################################
  ## Automation Name
  #
  ## One-line description matching the description: field.
  #################################################################
  ```
