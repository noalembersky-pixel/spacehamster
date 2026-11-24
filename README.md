# Space Hamster Run — website

Live at https://spacehamster.oatmealmorning.com (GitHub Pages, `main` branch, root).

The website has **no playable game** (decided 24 Nov 2026). It is a store page only:

- `index.html` (home) and `get/index.html` (the link the apps share) are the same store page.
  Both say "Coming soon to the App Store and Google Play" until a store goes live.
  Launch day: set `LIVE = { ios: true/false, android: true/false }` near the bottom of **both** files
  (and put the real App Store id in the `storeIos` link).
- `privacy/` and `support/` describe the app. Update `privacy/` whenever the app's analytics change.

## The game file (for the app builds only)

`tools/merge_guy_build.py` turns Guy's latest HTML file into the game file the apps bundle.
**Never write its output into this folder** (it would put the game back on the home page):

    python3 tools/merge_guy_build.py GUY_FILE.html /tmp/spacehamster-build

Then change the one `SHR_BUILD` line to `{ platform: 'android', version: 'X.Y' }` and copy the file to
`Desktop/Oatmeal Morning/Space Hamster Run/spacehamster-app/app-web/index.html`.
Feedback form link, share links and PostHog key are at the top of the script.

Made by Oatmeal Morning. © 2026 Oatmeal Morning.
