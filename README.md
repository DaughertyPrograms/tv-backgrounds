# TV backgrounds (Clean Home) - 2026-10-23

Pictures in `images/` become the background on the TVs. They cycle on the timer set in Clean Home Studio,
and the TVs check this folder for new pictures on their own.

## Where the TVs read from
Nothing to set up. In Clean Home Studio, set Scene > Background to **Web folder** with:

    https://raw.githubusercontent.com/DaughertyPrograms/tv-backgrounds/main

The repo must stay **public**. New pictures can take ~5 minutes to appear (GitHub caching).

## Albums
Every folder inside `images/` is an album (e.g. `images/Fall/`, `images/Winter/`). On the TV or in Clean Home Studio,
choose **All pictures** or one album. Pictures placed directly in `images/` show up as the album **Unsorted**.

## Adding or removing pictures
- Add: open an album folder on GitHub, then Add file > Upload files. JPG, PNG or WebP.
  New album: Add file > Create new file, type `images/AlbumName/` then any name, or upload with the folder name in the path.
- Delete: open the picture on GitHub, click the ... menu (top right) > Delete file, then Commit changes.
  To remove a whole album, delete every picture in it (GitHub drops empty folders by itself).
- The **Update manifest** action runs by itself and rewrites `manifest.json`. Nothing else to do.
- Best results: 16:9, at least 1920x1080 (larger is fine; keep the originals 4K+). The TV crops to fill the screen.
