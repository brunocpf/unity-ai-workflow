# Worked OpenSpec example: pause and resume

Illustrative documents, not implemented or accepted Unity functionality. Use the shipped unity-game schema. A real game's product contract owns targets/devices/locales.

## Capability baseline

`openspec/specs/pause/spec.md` is created when the first pause implementation is accepted. Before that, the new behavior belongs under `openspec/changes/add-pause/specs/pause/spec.md` as ADDED Requirements:

```markdown
## Purpose
Allow the player to suspend a single-player session while retaining responsive menu controls and preserving simulation state.

## ADDED Requirements

### Requirement: PAUSE-001 - Simulation suspension
The game SHALL suspend gameplay simulation while paused and retain responsive menu input and unscaled menu motion.

#### Scenario: Pause during a cooldown
- **WHEN** the player pauses while a cooldown is active
- **THEN** gameplay state and cooldown time remain unchanged until resuming
- **AND** the menu remains responsive

### Requirement: PAUSE-002 - Resume once
The game SHALL resume the same session exactly once per accepted resume command.

#### Scenario: Repeated input
- **WHEN** resume is triggered repeatedly during menu teardown
- **THEN** gameplay input and simulation resume once without duplicated subscriptions
```

Design links the existing clocks, pure ViewModel, mechanical bindings, authored UXML/USS, visual brief and localization contract. Tasks include pure-clock tests, real input/lifecycle integration and player visual inspection within the slice.

## Follow-up change

`openspec/changes/confirm-restart/` links the owning issue. Its proposal records the requested restart confirmation and excludes persistence changes. Its delta adds PAUSE-003: cancel retains the paused session; confirm restarts exactly once. PAUSE-001/002 remain regression requirements.

Resolve initial focus/back behavior from an established project policy or user answer before dependent UI work. The plan reuses existing MVVM/R3/Input System/LitMotion and extends the authored control/localized keys. No dependency upgrade is implied.

Tasks cover command/state scenarios, UI Builder preview, input/locale/reduced-motion player states, disposal, repeated confirm and cancellation. A passing pure test does not close visual or device criteria.

## Verification

Start verification.json with pending rows for every changed ID and required evidence kinds selected from the design. For example, PAUSE-003 needs automated checks plus visual and authoring evidence. Add PAUSE-001/002 rows when retaining regression evidence helps review. Every row uses actual reports/captures with hashes, commands/procedures, targets and run IDs; manual rows name the actual reviewer.

Run the mapped checks, inspect the resulting UI, reconcile defects, and obtain the source/spec fingerprint with the shipped helper. Acceptance mode must fail while visual review is pending. After all required verdicts pass, validate, check acceptance, archive and validate the merged baseline. A later request resumes from the updated capability spec, not from the original chat or completed task history.
