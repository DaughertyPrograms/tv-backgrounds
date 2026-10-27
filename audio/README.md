# Background music — 2026-10-27 V3

Peaceful loops for the Clean Home home screen. Each sub-folder is a category on the TV
(App Settings › Sound › Background music).

| Category | Track | Feel |
|---|---|---|
| Nature | night-field | warm low chords, a hush of wind, two distant crickets |
| Nature | gentle-rain | muffled rain heard from indoors, a few soft drips, quiet chords |
| Tech | soft-tech-drone | warm, slowly breathing low drone with a few far-off chimes |
| Tech | deep-space | very low drone, slow airy sweeps |
| Pads | warm-chords | slow pad chords (Cmaj9 · Am9 · Fmaj9 · Gsus2) |
| Pads | evening-glow | softer pad chords in D, 20 s per chord |

- **Royalty-free:** every track is original and fully synthesized by `tools/make_ambient.py`
  (no samples or third-party audio). Released under CC0 — free to use for anything.
- **Seamless:** each track loops every 240 s (all sounds wrap around the loop point). The file runs 4 s
  past the loop point with an exact copy of the opening; `loops.json` lists the loop point. At the loop
  point the TV starts its second player at the matching spot and crossfades over identical audio, so there
  is no gap and no two different chords ever sound together. Tracks you add without a `loops.json` entry
  get a gentle 6 s crossfade instead.
- **Volume-safe:** all tracks are mastered gently (−26 to −29 LUFS, no harsh highs),
  and the TV app never plays them above 60 % of its own output.

Add your own: drop an `.m4a` or `.mp3` into a folder here (a new folder = a new category).
Only add audio you have the rights to use. For the smoothest loop, export it at about −26 LUFS.
