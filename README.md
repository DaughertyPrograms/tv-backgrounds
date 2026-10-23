# TV backgrounds (Clean Home) - 2026-10-23

Pictures in `images/` become the background on the TVs. They cycle on the timer set in Clean Home Studio,
and the TVs check this folder for new pictures on their own.

## Where the TVs read from
Nothing to set up. In Clean Home Studio, set Scene > Background to **Web folder** with:

    https://raw.githubusercontent.com/DaughertyPrograms/tv-backgrounds/main

The repo must stay **public**. New pictures can take ~5 minutes to appear (GitHub caching).

## Adding or removing pictures
- Drop images into `images/` on GitHub (Add file > Upload files). JPG, PNG or WebP.
- The **Update manifest** action runs by itself and rewrites `manifest.json`. Nothing else to do.
- Best results: 16:9, at least 1920x1080 (larger is fine; keep the originals 4K+). The TV crops to fill the screen.
