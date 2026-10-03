# Profile art direction

This is a GitHub profile README, with original raster artwork inspired by the brutalist architecture, suspended geometry, and vermilion lighting of Remedy Entertainment's Control. No official game assets or logos are included.

## Assets

- `control-cover.png`: original cover generated with the built-in image generation tool. The exact prompt is recorded below.
- `hedron-study.gif`: original Blender-rendered 3D animation. 240 frames, 20 fps, twelve-second loop. Includes a rotating icosahedron and 14 floating concrete blocks. It is an atmospheric illustration, not a CFD or engineering result.
- `hedron-study-still.png`: stationary alternative. Replace the GIF reference in the README with this file to disable motion.
- The previous graphics are retained in assets for reference, but the README no longer uses them.

The profile now has six distinct visual sections: personal dossier, project evidence, research spotlight, method and tools, public activity, and contact. The original cover and smooth hedron remain. Repeated typography plates have been combined into fewer editorial boards.

`dossier-emblem.png` and `heat-sink-concept.png` are original Blender renders. The heat sink is conceptual geometry: the red lighting is artistic and conveys no measured temperature or CFD results. `project-captures.json` records public source revisions, demo inputs, and capture provenance. All three project panels use genuine interface screenshots, with links to full captures for inspection.

The new editorial panels keep every heading, label, numeral, metric, photo, and reading surface stationary. A red registration sweep is confined to the empty bottom margin. It follows a twelve-second cosine cycle at 20 fps, slowing to zero at both ends rather than jumping from right to left. Phases are offset across panels. A fixed image palette prevents text and screenshot colours from flickering between GIF frames. Title wipes, floating text, cycling labels, and moving principle highlights remain removed.

The 3D loop now lasts twelve seconds rather than four, rendered with twice the previous sampling and an exact 50 ms GIF cadence. Cyclic motion avoids an abrupt loop reset. These choices reduce visual distraction; they are not a guarantee of comfort for every viewer. GitHub README images cannot expose reliable pause controls or honor reduced-motion CSS. The profile therefore links to `STILL.md` at the top, providing the complete same-content design with zero animated assets.

All meaningful profile copy remains selectable Markdown inside expandable descriptions and text versions. Images have descriptive alt text, and contact/project links remain independent of the artwork. GitHub controls the surrounding page styling. No external image services, JavaScript, or CSS dependencies are required to display the profile.

Responsive `<picture>` elements select compact stationary panels below 600 pixels, with larger stacked headings and labels instead of shrinking desktop boards. The desktop artwork remains the fallback. Both profile versions use the same compact PNGs; the still version also replaces the hedron loop. This uses [GitHub-supported picture markup](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax). Full interface captures and selectable descriptions remain available at every width.

## Rebuild the editorial profile

The source copy lives in `profile/content.json`. Run `node tools/assemble_profile.mjs` to regenerate both README variants without duplicating or losing selectable descriptions. The complete still version uses the same copy and all static PNG assets. New one-line project captions and full-capture links remain visible outside expandable sections, including on narrow screens.

Install `tools/requirements.txt` in a Python 3.11 environment. On Windows with Arial and Impact installed, run `python tools/render_profile.py` to compose the dossier, project, research, method, and contact panels. Genuine captures must exist first; this renderer fails rather than substituting an invented screenshot. Run Blender 4.2 with `--background --python tools/render_editorial_3d.py` to rebuild the original emblem and conceptual heat sink. The original typography renderer remains available for archived assets but its plates are no longer the main profile layout.

Run `python tools/render_mobile.py` after the desktop renders to build the compact static panels, then assemble both Markdown files. Run `python tools/verify_motion.py` to check twelve-second timing, stationary reading regions, and sweep continuity across all seven editorial animations.

## Public activity refresh

`python tools/activity.py --username suren1013 --output-dir assets` fetches the public contribution calendar, validates dates and tooltip counts, and generates `activity-data.json`, `activity-landscape.png`, `activity-landscape-mobile.png`, and `activity-summary.md`. Both activity images are stationary. Heights and colours represent GitHub intensity levels; totals sum the publicly displayed daily counts. These numbers do not imply the contents of private repositories or measure engineering quality.

The GitHub Actions workflow runs at `02:00 UTC` (07:30 IST) and supports manual dispatch. It uses the repository token for Git commits, needs no personal token, and stages only the four activity files. Scheduling becomes active when the workflow reaches the repository's default branch; GitHub may delay scheduled runs. Fetch, parse, and render failures occur before output replacement, preserve the previous successful artwork and refresh date, and fail the job visibly. Source markup changes or a public calendar more than fourteen days out of date are rejected. Linux rendering installs DejaVu fonts; the renderer uses those when Windows fonts are unavailable.

Run `python -m unittest discover -s tests -v` and `node tools/verify_profile.mjs` for calendar validation, failure preservation, source-copy retention, and asset checks.

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

