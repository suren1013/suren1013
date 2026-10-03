# Profile art direction

This is a GitHub profile README, with original raster artwork inspired by the brutalist architecture, suspended geometry, and vermilion lighting of Remedy Entertainment's Control. No official game assets or logos are included.

## Assets

- `control-cover.png`: original cover generated with the built-in image generation tool. The exact prompt is recorded below.
- `hedron-study.gif`: original Blender-rendered 3D animation. 240 frames, 20 fps, twelve-second loop. Includes a rotating icosahedron and 14 floating concrete blocks. It is an atmospheric illustration, not a CFD or engineering result.
- `hedron-study-still.png`: stationary alternative. Replace the GIF reference in the README with this file to disable motion.
- The previous graphics are retained in assets for reference, but the README no longer uses them.

The twelve raster typography panels keep every heading, label, numeral, metric, and reading surface stationary. Each panel restores a red registration sweep confined to the empty bottom margin. It follows a twelve-second cosine cycle at 20 fps, slowing to zero at both ends rather than jumping from right to left. Panel phases are offset to avoid synchronised sweeps throughout the page. Title wipes, floating text, cycling status labels, and moving principle highlights remain removed. Red accents are softer, and secondary labels are brighter for readability.

Two additional panels develop the existing profile content: a five-stage engineering workflow (question, model, simulate, validate, build) and research directions that distinguish the current thermal/CFD focus from longer-term aerospace interests. Collaboration starting points provide concrete ways to discuss a project without adding unsupported claims of experience. The stationary version includes the same new content and same-name PNG artwork.

The 3D loop now lasts twelve seconds rather than four, rendered with twice the previous sampling and an exact 50 ms GIF cadence. Cyclic motion avoids an abrupt loop reset. These choices reduce visual distraction; they are not a guarantee of comfort for every viewer. GitHub README images cannot expose reliable pause controls or honor reduced-motion CSS. The profile therefore links to `STILL.md` at the top, providing the complete same-content design with zero animated assets.

All meaningful profile copy remains selectable Markdown inside expandable descriptions and text versions. Images have descriptive alt text, and contact/project links remain independent of the artwork. GitHub controls the surrounding page styling. No external image services, JavaScript, or CSS dependencies are required to display the profile.

Rebuild the typography panels with `./tools/render_typography.ps1` from PowerShell on Windows. This renderer uses System.Drawing, the installed Impact and Arial fonts, and FFmpeg. Override its `-FFmpeg` argument if FFmpeg lives elsewhere. It generates fresh raster frames from text and drawing commands; it does not modify the cover or the Blender artwork.

## Rebuild the animation

Requirements: Blender 4.2 and FFmpeg. The renderer uses the static Arial Bold font installed on Windows at C:/Windows/Fonts/arialbd.ttf; adjust this path on other platforms.

Run from the repository root:

```powershell
& 'C:/Program Files/Blender Foundation/Blender 4.2/blender.exe' --background --python tools/render_control.py
& 'C:/Program Files/Shutter Encoder/Library/ffmpeg.exe' -y -framerate 20 -i build/frames/%04d.png -filter_complex '[0:v]split[a][b];[a]palettegen=max_colors=128:stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=3' -frames:v 240 -loop 0 assets/hedron-study.gif
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

