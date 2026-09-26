# Video reference → 3D animation

Veo is Google's video-generation model exposed through Gemini APIs. It produces video, not an FBX/BVH skeleton. Its documentation offers reference-image and first/last-frame guidance, with model-dependent limits; record the exact model and accepted video instead of relying on a repeatable seed. [Veo documentation](https://ai.google.dev/gemini-api/docs/veo?hl=en).

Recommended motion brief: one subject, whole body visible, static camera, uncluttered contrasting background, visible floor and contact points, constant speed, one action, no cuts, little occlusion, clear start/end pose. Request a side or three-quarter view appropriate to the action. Multiple independently generated views are references, not synchronized motion-capture cameras.

Workflow:

1. Generate/select the reference clip and inspect temporal anatomy/contact continuity. Reject impossible motion before animation work.
2. Extract a contact sheet and mark anticipation, contact, apex, recovery, and intended gameplay timing.
3. Convert those observations into an explicit animation spec: duration, frame rate, root trajectory, foot/hand contact windows, weapon arcs, loop/additive policy, and responsiveness requirements.
4. Choose direct Blender keyframing for short stylized actions, an existing retargetable motion source for common locomotion, or a separately evaluated video-to-motion system for longer natural motion.
5. If estimating motion, calibrate scale and floor, map skeletons, solve depth/occlusion ambiguities, then clean jitter, foot sliding, penetration, and root drift. Generated video may make estimation worse through changing anatomy.
6. Retarget onto the project's stable deform skeleton; use IK for contact cleanup. Bake the result and simplify curves within a measured pose-error tolerance.
7. Import into Unity, check Humanoid/Generic mapping, in-place/root-motion policy, clip looping, blend transitions, and gameplay interruption behavior.
8. Validate at gameplay camera distance and playback speeds. Align combat windows with the gameplay simulation; do not make visual animation events the sole authoritative combat state in networked or replayable games.

Keep source video, timing notes, .blend, export, and acceptance capture linked by asset ID. No connected Gemini video-generation tool was identified in this session; implementing this branch requires a configured Gemini API client or equivalent supported integration. This research did not submit paid generation jobs.
