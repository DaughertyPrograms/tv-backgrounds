# TV backgrounds (Clean Home) - 2026-10-23

Pictures in `images/` become the background on the TVs. They cycle on the timer set in Clean Home Studio,
and the TVs check this folder for new pictures on their own.

## One-time setup
1. Create a **public** GitHub repo (for example `tv-backgrounds`) and upload everything in this folder.
2. Repo **Settings > Pages**: Source = *Deploy from a branch*, Branch = `main`, folder `/ (root)`. Save.
3. Same page, **Custom domain**: `tv.daugherty.pro`. Save, then tick **Enforce HTTPS** once it's offered.
4. In **Cloudflare > daugherty.pro > DNS**, add a record: Type `CNAME`, Name `tv`, Target `<your-github-username>.github.io`.
   Set it to **DNS only** (grey cloud) until GitHub shows the certificate is issued; you can turn the proxy on afterwards.
5. Check `https://tv.daugherty.pro/manifest.json` loads in a browser.

## Adding or removing pictures
- Drop images into `images/` on GitHub (Add file > Upload files). JPG, PNG or WebP.
- The **Update manifest** action runs by itself and rewrites `manifest.json`. Nothing else to do.
- Best results: 16:9, at least 1920x1080 (larger is fine; keep the originals 4K+). The TV crops to fill the screen.

## Why tv.daugherty.pro and not daugherty.pro/TV
GitHub Pages can only own a whole (sub)domain. Serving it under `/TV` on the main site would need a
Cloudflare Worker in front of daugherty.pro. The subdomain is simpler and free.
