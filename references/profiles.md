# Optional game profiles

All profiles retain the [professional baseline](engineering-baseline.md); none is a shortcut around architecture, quality or ownership. No fixed workflow can pre-solve every game. Keep optional modules with explicit entry conditions and acceptance gates.

| Profile | Add only when needed | Critical proof |
|---|---|---|
| 2D pixel game | PPU/palette/tileset contracts, camera and atlas rules | No shimmer/seams at supported scales |
| 3D action | Animation/root-motion policy, collision proxies, LODs | Contact quality and gameplay responsiveness |
| Multiplayer | Authority model, protocol versions, prediction/reconciliation | Latency/loss/reconnect and cheating boundaries |
| Deterministic/replay | Controlled ticks/RNG/numeric policy, event/input records | Cross-run and cross-platform equivalence |
| Large world | Streaming/content lifetimes, navigation chunks, origin strategy | Memory ceiling and seam transitions |
| Mobile/Web | Compression, startup/download/memory budgets, platform input | Real-device/browser performance |
| Console | Platform SDK, certification, signing, save/user lifecycle | Platform-required validation |
| XR | Interaction/world-space UI, locomotion comfort, device rendering | Target headset performance and interaction |
| Cinematic/facial | Blendshapes, facial rig, lip sync, camera/editing | Face/deformation review and export fidelity |
| Live content/modding | Compatibility IDs, catalog update/rollback, trust boundaries | Old client/new content and rollback tests |
| Audio/VFX | Separate briefs, routing/voice budgets, effect quality levels | Mix clarity, visual readability, runtime budget |
| Extended accessibility / localized media | Additional input alternatives, localized voice/art, script-specific layouts | User-facing navigation/readability on target; basic text [localization](localization.md) already belongs to the baseline |

Networking, audio, platform services, monetization, and facial motion are not supplied by the requested art generators. They use the same brief → implementation → evidence model with their own adapters and platform skills.

Package presets live in [dependencies](dependencies.md). Each adopted profile declares supported targets, added dependencies/lifetimes and acceptance fixtures; create only used modules.
