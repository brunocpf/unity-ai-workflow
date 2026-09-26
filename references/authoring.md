# Editor authoring contract

**The delivered project must be usable by an Editor-based author.** Save authored layouts, reusable visual configurations and tuning as Unity assets. Pure Core/Application/Presentation and runtime spawning remain the architecture; they do not require recreating the authored world in code. Runtime correctness and authoring usability are separate release gates.

## Defaults by responsibility

| Concern | Default authoring surface | Runtime responsibility |
|---|---|---|
| Level/environment | Saved gameplay scene, visible environment, camera/lighting, boundaries and spawn markers | Scene loading, session wiring and explicitly procedural population |
| Character/enemy/projectile/pickup | Prefab with renderers, colliders, animator, sockets and view adapters wired | Instantiate or rent the authored prefab, bind state, release/reset |
| Shared visual family | Base prefab plus shallow, purposeful variants | Select the variant; avoid rebuilding component hierarchies |
| Enemy/weapon/wave/upgrade tuning | Cohesive validated ScriptableObject definitions and catalogs | Compile immutable pure configuration once per session/load boundary |
| Local layout/placement override | Serialized scene/prefab instance data | Convert coordinates/parameters at the Unity boundary |
| Mutable health, currency, cooldown | Session/domain state, never a writable definition asset | Application/Core owns transitions |
| UI | Saved UXML/USS, control library and authoring previews | Construct/bind through the selected UI factory; no GameObject prefab requirement |
| Procedural world/mesh/VFX or ECS | Saved generator settings/seed, preview tools/gizmos; baking where appropriate | Generate the intended dynamic result within budgets |

Prefabs store reusable GameObject configuration; variants inherit a base with deliberate overrides. Keep variant chains understandable, and keep authored wrapper/variant prefabs separate from imported model assets. [Unity prefab variants](https://docs.unity3d.com/6000.7/Documentation/Manual/PrefabVariants.html).

A small bootstrap scene may contain services only when the actual gameplay scenes and prefab previews remain authored and discoverable. The default is not an almost-empty game scene with all visible content assembled in Start. Do not put every scene prop in a prefab or every number in its own ScriptableObject: reuse, shared identity and the author's editing task determine asset granularity. Algorithm constants/invariants stay in C#; frequently tuned design values use an authoring surface.

## Definitions into pure configuration

`EnemyDefinition.asset → validation/compilation at the Unity boundary → immutable EnemyConfig → Application/Core`; a separate Unity-side ID-to-prefab mapping supplies visuals. [Definition example](../examples/Unity/Runtime/EnemyDefinition.cs) and [pure configuration](../examples/Core/Combat/EnemyConfig.cs) show the seam. Definition classes live under Unity/Runtime/<feature>/Authoring; the asset instances live under Content/<feature>/Definitions. Core never references ScriptableObject, GameObject, Sprite, AnimationCurve or other Unity types.

Definitions carry stable IDs, units/tooltips, defaults and necessary asset references. Clone editable collections into immutable/runtime-owned data; translate curves/vectors into pure values when needed. Expose read-only runtime configuration, never the serialized authoring collection as mutable game state. Changes during Play do not silently rewrite shared definitions; default to compiling on session start. Explicit live-tuning tools need a separate apply/reset policy.

Validate local ranges/nulls and cross-asset IDs/references, wave ordering, prefab components and catalog membership. Inspector Min/Range attributes are feedback, not complete validation. Use the same substantive validator during authoring, preflight/build and startup. Build validation follows the actual scene/prefab/catalog references selected for the build, including overrides; validating fixed seed assets by path is insufficient. Missing/invalid required data fails with the asset path, ID and field. Do not silently substitute hard-coded tuning. OnValidate is not a bootstrap, file generator or global catalog scanner. Batch Editor validation covers assets not currently loaded in a scene.

One authoritative source per value: do not repeat max health in both a prefab and its definition, or keep a C# enemy roster beside a catalog. If prefab-instance overrides are a feature, define the precedence and validation explicitly. Preserve IDs/GUIDs on rename; serialized-field changes need migrations or FormerlySerializedAs where applicable. A new definition using existing behavior should not require adding a new switch case just to be discoverable.

## Prefab factories and previews

The Composition root supplies typed factories/pools with authored prefab references and dependencies. Unity.Runtime owns the view components. Bind a spawned instance before gameplay updates; Awake may validate/cache structural references, while OnEnable must not assume injected session services already exist. Choose one documented activation sequence and test first spawn and pooled reuse. Reset subscriptions, motion, physics, timers and transient VFX on return. Do not create one DI container per projectile.

Preview visuals must not require a live service container. Prefab Mode and an authored gallery/test scene show the intended pose, scale, sockets/colliders and representative effects; optional Editor preview tooling lives in Game.Editor and creates no production services. Level gizmos expose spawn regions and bounds. Editable Animator, materials and VFX assets stay discoverable. Runtime services and bindings are still composed in code.

## Generation and preservation

Treat **generated artifacts** and **authored assets** as different ownership classes, regardless of whether AI originally created them.

- Initial scaffold: create missing assets, save them through Unity Editor APIs, preserve metadata. Repeating setup does not reset existing scenes, definitions or prefabs.
- Regenerable outputs: own an explicit path such as Assets/Game/Generated/<feature>/, with source inputs, generator version and ownership manifest. Keep human overrides outside the replaceable portion, for example in variants or authored wrapper assets.
- Authored assets: normal builds consume them. Explicit edit/migration tools update only intended fields, preserve unrelated values/GUIDs, support Undo where applicable, mark/save the correct assets and report changed files. Recreating a whole scene to change one field is not the default.
- A rebuild or ordinary Play entry never regenerates authored scenes/prefabs from hard-coded defaults. Explicit regeneration needs a preview/diff and a stated ownership boundary. Refuse an unexpected collision rather than deleting unowned content. Baked output may be regenerated when its authored inputs remain authoritative.

PrefabUtility and scene/asset Editor APIs save procedural authoring results as real assets. Update-in-place still needs reference/override checks; preserving a filename alone is not proof that nested object references survived. [SaveAsPrefabAsset](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/PrefabUtility.SaveAsPrefabAsset.html).

Procedural gameplay, streaming, data-oriented rendering, headless simulation and temporary test fixtures are valid exceptions to particular assets. Record the concrete reason, source of tuning, preview path and tests in the feature contract. Whole-feature runtime hierarchy construction needs this explanation; convenience of writing C# is insufficient. Routine factory-created service/host objects need no exception.

## Acceptance

Use the [authoring acceptance checks](validation.md#editor-authoring-acceptance). Document scene, prefab, definition and generator locations in docs/authoring.md. A successful player build cannot waive this gate. Preservation tests compare against the captured pre-operation values/bytes, not hard-coded seed defaults: a valid designer edit must keep the suite green. Include a valid non-default tuning edit, a referenced replacement definition, and rejection of invalid replacement data; do not accidentally require the original asset count or tuning forever.
