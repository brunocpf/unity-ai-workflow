# Optional libraries

Use only when the feature needs the capability. [Dependency defaults](dependencies.md) own pins, adoption gates and presets.

The Default column records the selected decision. The exception column is a threshold to investigate, not an invitation to compare every product on every feature.

| Use case | Default | Escalate only when… |
|---|---|---|
| Local UI templates/styles/content | Implement UI/module preloading through Content Directories plus constructor-time read-only template lookup; UXML owns USS | For a minimal or older-editor profile, direct references are the selected fallback. For remote delivery/patching or an existing Addressables dependency, evaluate Addressables behind the content contract. The kit includes a Content Directory loading adapter; project build/registration and player acceptance remain required. Direct references and Addressables require their selected integration. |
| Character clips | Animator + imported clips | **Animancer** is the selected third-party option for code-directed clip playback when controller maintenance becomes a demonstrated cost. |
| IK and procedural posing | Unity Animation Rigging | A concrete creature/locomotion solver is beyond its constraints; evaluate a specialist solver against a recorded animation scenario. |
| Scripted cutscenes | Unity Timeline + Cinemachine | A feature needs procedural orchestration; coordinate with UniTask while keeping timeline and camera ownership explicit. |
| Ordinary 3D navigation | Unity AI Navigation | Grid/graph-based worlds or navigation requirements exceed the chosen NavMesh approach: evaluate **A* Pathfinding Project**. |
| Small tactical-grid pathfinding | Small pure A* implementation with rule tests | Rich graph updates, large-scale navigation or tooling justify A* Pathfinding Project. Don't custom-build a production navigation suite. |
| NPC behavior | Small explicit state machine in Core | Many designer-authored branching behaviors justify a dedicated behavior-tree authoring evaluation. No mandatory global AI framework. |
| Dialogue-heavy games | **Yarn Spinner** | A project has a different established narrative runtime; keep that runtime behind a dialogue adapter. Use a custom UITK view for this architecture. |
| Saves/settings | Versioned DTOs + repository-owned migrations; **Unity's Newtonsoft Json package** for structured JSON | Binary size/speed is a measured issue. Keep serialization behind a port; don't serialize scene graphs or reactive objects. |
| Basic audio | Unity AudioMixer and AudioSource adapters | A dedicated audio workflow needs interactive music/events/banks: **FMOD** is the selected middleware candidate. |
| Inspector productivity | Built-in inspectors + targeted custom UITK editors | Repeated authoring overhead justifies **Alchemy**; keep editor helpers separate, and explicitly review any serialization dependency. |
| Pooling | UnityEngine.Pool in adapters | Measured use cases require a specialist pool. No global object-pool service in Core. |
| Ordinary collections/querying | BCL collections; explicit loops in measured hot paths | Profiling demonstrates a need for a specialized allocation/performance library; record a benchmark before adding one. |
| Cross-feature messages | Explicit ports and R3 scoped streams | A genuine broker topology requires **MessagePipe**. It is not a second default event bus. |
| Small cooperative multiplayer | Unity Netcode for GameObjects + explicitly selected session/transport services | Competitive prediction requirements drive a **Photon Fusion** evaluation. Neither choice is universal or transport-independent. |
| Very large simulations | GameObject architecture with profiled jobs/Burst where useful | Measured entity counts and team skills justify an Entities/DOTS profile. Treat this as an architectural choice, not a late optimization package. |
| Analytics, purchases, ads, voice | No package until required | Add the relevant platform/service SDK behind an adapter using the available Unity skill. Confirm supported targets and configuration in the project's compatibility record. |

Official capability sources: [Animation Rigging](https://docs.unity3d.com/Packages/com.unity.animation.rigging@1.3/manual/index.html), [Animancer](https://kybernetik.com.au/animancer/docs/), [AI Navigation](https://docs.unity3d.com/ja/6000.0/Manual/com.unity.ai.navigation.html), [A* Pathfinding Project](https://www.arongranberg.com/astar/), [Yarn Spinner installation](https://github.com/YarnSpinnerTool/YSDocs/blob/main/docs/yarn-spinner-for-unity/installation-and-setup/README.md), [Yarn localization](https://github.com/YarnSpinnerTool/YSDocs/blob/main/docs/yarn-spinner-for-unity/assets-and-localization/README.md), [Unity Newtonsoft Json](https://docs.unity3d.com/Packages/com.unity.nuget.newtonsoft-json@3.2/manual/index.html), [FMOD](https://www.fmod.com/unity), [Alchemy](https://github.com/annulusgames/Alchemy), [MessagePipe](https://github.com/Cysharp/MessagePipe), [Netcode for GameObjects](https://docs.unity3d.com/Packages/com.unity.netcode.gameobjects@2.7/manual/index.html), [Photon Fusion](https://doc.photonengine.com/fusion/current/getting-started/fusion-intro). Content and engine architecture follow their task references. Pricing and commercial license eligibility must be checked when adopting a paid tool; no prices or entitlements are assumed here.
