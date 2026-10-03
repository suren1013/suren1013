# Profile art direction

This is a GitHub profile README, with original raster artwork inspired by the brutalist architecture, suspended geometry, and vermilion lighting of Remedy Entertainment's Control. No official game assets or logos are included.

## Assets

- `control-cover.png`: original cover generated with the built-in image generation tool. The exact prompt is recorded below.
- `hedron-study.gif`: original Blender-rendered 3D animation. 72 frames, 18 fps, four-second loop. Includes a rotating icosahedron and 14 floating concrete blocks. It is an atmospheric illustration, not a CFD or engineering result.
- `hedron-study-still.png`: stationary alternative. Replace the GIF reference in the README with this file to disable motion.
- The previous graphics are retained in assets for reference, but the README no longer uses them.

All meaningful profile copy remains selectable Markdown. Images have descriptive alt text, and contact/project links remain independent of the artwork. GitHub controls the surrounding page styling. No external image services, JavaScript, or CSS dependencies are required to display the profile.

## Rebuild the animation

Requirements: Blender 4.2 and FFmpeg. The renderer uses the static Arial Bold font installed on Windows at C:/Windows/Fonts/arialbd.ttf; adjust this path on other platforms.

Run from the repository root:

```powershell
& 'C:/Program Files/Blender Foundation/Blender 4.2/blender.exe' --background --python tools/render_control.py
& 'C:/Program Files/Shutter Encoder/Library/ffmpeg.exe' -y -framerate 18 -i build/frames/%04d.png -filter_complex '[0:v]split[a][b];[a]palettegen=stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=3' -loop 0 assets/hedron-study.gif
Copy-Item build/frames/0001.png assets/hedron-study-still.png
```

Intermediate frames are ignored by Git.

## Cover generation prompt

Built-in image generation tool; opaque background.

Use case: stylized-concept
Asset type: ultra-wide GitHub profile cover, 1536x640 landscape.
Primary request: a premium cinematic title card inspired by Remedy Entertainment's Control: monumental brutalist concrete architecture, paranormal suspended cuboids, one enormous dark fractured polyhedral hedron on the RIGHT half, a deep vermilion light slicing into an ash-grey concrete chamber. Original artwork, no game screenshots.
Composition: restrained editorial title card. Left half is dark charcoal negative space, right half detailed cinematic physical architecture and suspended concrete monoliths. Sharp photographic concrete texture, volumetric dust, physically lit 3D materials, sophisticated film art direction. Very limited palette black, warm grey, bone white, intense vermilion.
Text verbatim: "SURENDHER" large condensed white uppercase on the left, smaller line below "MECHANICAL ENGINEERING / COMPUTATION". Small top-left "INDEPENDENT ENGINEERING PRACTICE", small bottom-left "PHYSICS → MODELS → WORKING SYSTEMS".
Avoid: SVG illustration, gradients-as-design, gaming HUD, cyberpunk neon, decorative icons, logos, official game branding, badges, illegible text, cheesy sci-fi. Architecture and typography should feel like a museum exhibition poster and a Control art book cover.

