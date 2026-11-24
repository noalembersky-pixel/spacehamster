"""Make the game file for an app build (Android or iPhone) from the web game file.

    python3 tools/merge_guy_build.py GUY_FILE.html /tmp/spacehamster-build      # web game file
    python3 tools/make_app_build.py /tmp/spacehamster-build/index.html OUT_DIR --platform ios --version 1.0

What it changes (exact text replacements; stops with an error if the text moved):
  - the one SHR_BUILD line -> { platform: '<platform>', version: '<version>' } (analytics tag + /get/ share link)
  - iOS only: SHARE uses the Capacitor Share plugin (the iPhone share sheet), because the
    in-app web view can't be trusted to have navigator.share.
Android needs no shim: its own shell adds navigator.share (ShrNative bridge in MainActivity.java).

Never write the output into the website folder: the website has no game (decided 24 Nov 2026).
"""
import argparse
import pathlib
import sys

ap = argparse.ArgumentParser()
ap.add_argument('src')
ap.add_argument('out_dir')
ap.add_argument('--platform', required=True, choices=['android', 'ios'])
ap.add_argument('--version', required=True)
a = ap.parse_args()

s = pathlib.Path(a.src).read_text(encoding='utf-8')


def sub(old, new):
    global s
    n = s.count(old)
    if n != 1:
        sys.exit(f'STOP: expected 1 match, found {n}, for: {old[:100]!r}')
    s = s.replace(old, new)


sub("const SHR_BUILD = { platform: 'web', version: '' };",
    f"const SHR_BUILD = {{ platform: '{a.platform}', version: '{a.version}' }};")

if a.platform == 'ios':
    sub('</body>', """<script>
/* iOS app: SHARE opens the iPhone share sheet through the Capacitor Share plugin. */
(function () {
  var P = window.Capacitor && window.Capacitor.Plugins && window.Capacitor.Plugins.Share;
  if (!P) return;
  navigator.share = function (d) {
    d = d || {};
    return P.share({ title: d.title || 'Space Hamster Run', text: d.text || '', url: d.url || '', dialogTitle: 'Share Space Hamster Run' })
      .catch(function () {});
  };
})();
</script>
</body>""")

out = pathlib.Path(a.out_dir)
out.mkdir(parents=True, exist_ok=True)
(out / 'index.html').write_text(s, encoding='utf-8')
print('ok:', out / 'index.html', a.platform, a.version, round(len(s.encode()) / 1e6, 2), 'MB')
