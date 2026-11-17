# Amos Abiodun portfolio website

A plain HTML, CSS and JavaScript site. No frameworks, nothing to install to view it.

## Folders

- `dist/` is the finished website. Open `dist/index.html` in a browser to view it. Upload the contents of `dist/` to any host (GitHub Pages, Netlify, cPanel) to put it online.
- `dist/css/site.css` holds all styling. The colours for dark and light mode are at the very top.
- `dist/js/site.js` holds the animations, theme switch, gallery viewer and contact form.
- `dist/img/` holds the photos and logos.
- `build.py` generates every page in `dist/` from one place, so the header, footer and menus stay identical.

## Changing things

The safest way is to edit `build.py` and run it:

    python3 build.py

- Text on a page: find the page function (`page_home`, `page_about`, `page_speaking`, ...) and edit the wording.
- Add a gallery photo: put the image in `dist/img/`, then add one line to the `GALLERY` list: file name, filter category, label, caption.
- Add a project: add an entry to the `PROJECTS` list.
- Add an award or certificate: add to `AWARDS` or `CERTS`.
- Numbers on the home page: edit `STATS`.
- Contact details: the constants at the top (`EMAIL`, `PHONE_SHOW`, `WA`, `LINKEDIN`, `GITHUB`).

You can also edit the `.html` files in `dist/` directly, but running `build.py` later will overwrite those edits.

Keep photos under about 1400 pixels on the long side so pages load fast.

## Putting it online (GitHub and Netlify)

1. Create a public repository on GitHub and upload everything in this folder (`build.py`, `netlify.toml`, `README.md` and the `dist` folder).
2. On Netlify, import that repository. The `netlify.toml` file already tells Netlify to publish the `dist` folder, so leave the build command empty.
3. In Netlify's site settings, change the site name to `amosabiodun` so the address is `https://amosabiodun.netlify.app`.

If that name is taken, pick another, then set `SITE_URL` at the top of `build.py` to the address you got and run `python3 build.py` before uploading.

## Search engines

These files are generated for you on every build: `dist/sitemap.xml`, `dist/robots.txt`, a canonical link and structured data on every page, and the link preview image `dist/img/share.jpg`.

After the site is live, add it to Google Search Console (search.google.com/search-console), submit `sitemap.xml`, and request indexing of the home page.

## Moving to amosabiodun.com

1. Add the domain in Netlify's domain settings and make it the primary domain. Netlify then redirects the old netlify.app address to it.
2. Change `SITE_URL` at the top of `build.py` to `https://amosabiodun.com`, run `python3 build.py`, and push the changes to GitHub.
3. Add the new domain to Google Search Console and submit the sitemap again.

## Updating the live site

The live site is built by Netlify from your GitHub repository, so any change you push to GitHub goes live about a minute later.

1. Make the change (edit `build.py` and run `python3 build.py`, or replace files in `dist/`).
2. On GitHub, open the repository, choose Add file, then Upload files, and drag in the changed files with the same folder structure (for example the `dist` folder). Files with the same name are replaced.
3. Write a short commit message and choose Commit changes.

With Git on your computer instead: `git add .`, then `git commit -m "Describe the change"`, then `git push`.

## Updating your CV

The download buttons point to `dist/Amos_Abiodun_CV.pdf`. To update the CV, replace that file with the new PDF, keeping the same file name, and push it to GitHub.
