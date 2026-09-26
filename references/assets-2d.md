# Images, textures and pixel art

### Image generation for textures and sprites

Generate against an art bible: palette, contrast, lighting direction, perspective, detail scale, outline policy, and example accepted assets. Keep prompts and reference images with the result. Prefer editing an accepted reference to starting every related asset from scratch.

For albedo, request neutral illumination; inspect for unwanted baked highlights and shadows. Generate or derive physically meaningful roughness/metallic/normal maps in a controlled material workflow rather than assuming a colored image is a valid PBR set. Test tiling by repeated preview; prompting “seamless” is not verification. Bake/project textures against the final UV layout when painting a specific mesh.

Import color textures as color and data maps as linear where required; use the proper normal-map importer. Map channels to the chosen URP/HDRP shader, including smoothness versus roughness conventions. Check alpha fringes, mip bleeding, compression, atlas padding, and target memory. A 4096² RGBA8 texture is 64 MiB uncompressed before mipmaps; generated resolution is not a free quality upgrade.

For cutout sprites, icons, decals and VFX, explicitly prompt: **“Export PNG with a real transparent alpha channel outside the subject; no background, no painted checkerboard, no baked backdrop.”** Some generators need this request on every generation/edit. Check the decoded file actually has non-opaque alpha; RGB artwork depicting a checkerboard is not transparent. Preview on light, dark and colored backgrounds, inspect edge halos and partially transparent pixels, and regenerate or mask in an image editor if necessary. Preserve intentional opaque backgrounds; do not indiscriminately remove matching colors inside the subject. Verify alpha survives export, Unity import and atlas packing.

For non-pixel sprite sequences, verify consistent bounds, pivot, scale, transparency, and frame identity. Image generation is useful for isolated images and references, but independent frame generation does not guarantee coherent animation.

For custom sprite/particle shaders, also run the [renderer tint/alpha fixture](visual-fixtures.md#sprite-and-particle-color-gallery). Correct source transparency and successful import do not prove that the shader uses SpriteRenderer tint or ParticleSystem vertex color.

### PixelLab for pixel art

PixelLab exposes character directions, animations, tilesets, isometric tiles, and image-editing workflows through MCP. The service documentation describes asynchronous jobs; poll the returned ID and archive the completed files. [PixelLab MCP](https://www.pixellab.ai/mcp), [integration options](https://www.pixellab.ai/docs/ways-to-use-pixellab).

Set logical pixel dimensions, view angle, character height, pixels-per-unit, palette, outline, light direction, direction count, animation names, and frame timing before generation. Build a representative character + walk + terrain + object first and approve the visual grammar before a full asset set.

Animate the same character identity. Reuse existing terrain/base tile identifiers for transitions where the tool supports them. Check every direction, feet alignment, silhouette consistency, tile adjacency, corners, and seams. Never assume arbitrary sprite-sheet ordering: consume metadata or define and verify a frame map.

Normalize palette and clean pixels in PixelLab or an editable pixel-art source tool. Use nearest-neighbor for pixel resizing. In Unity, configure Sprite import, Point filtering, suitable compression, explicit PPU and pivots, and normally no mipmaps for screen-aligned pixel art. World-space/minified art may need a different policy. Validate camera scaling and atlas packing together; Pixel Perfect Camera configuration is a game/render-profile choice.

Terrain tile rules and collisions are authored data. Generated Wang tiles do not automatically create correct Unity RuleTiles. Build that mapping, then exercise representative neighbor combinations and collisions in a test scene.
