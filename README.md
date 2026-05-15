# Kodi English Repository

This repository is a GitHub Pages Kodi add-on feed focused on the English
packages copied from the Dutch release line.

This repo keeps one untouched vanilla Fen Light copy under the original
`plugin.video.fenlight` ID as a known-good baseline, and uses the
`.kodienglish` suffix for the English working copy and the other forked add-ons.

## Addons In This Repo

Current source-tree versions:

- `plugin.video.fenlight` `2.0.16.1004`
  Vanilla Fen Light package kept as the known-good baseline with repo-wide bundled key updates plus TorBox Web Download cloud support.
- `plugin.video.fenlight.kodienglish` `2.0.16.1014`
  Working copy of vanilla Fen Light for the English-focused fork. It now also
  carries the newer Trakt/auth hardening, stable Trakt list-id routing, QR
  auth flows for Trakt, Real-Debrid, Premiumize, and AllDebrid, plus the
  playback properties and active-addon routing needed for next-episode OSD support.
  It now also guards duplicate Trakt re-authorization prompts, skips watched-indicator
  refresh on invalid Trakt payloads, rotates auth QR image filenames per device URL
  so Kodi refreshes changed codes, and brings the latest Extras trailer fallback and
  fullscreen-stop behavior into the English working copy. It now also refreshes
  the Trakt and Real-Debrid QR-backed auth prompts with styled Trakt QR cards and
  the latest activation URL / clipboard behavior, and adds TorBox Web Download
  cloud scraping, browsing, resolving, and deleting for web-hosted uploads. It
  now enables TorBox Search Cloud Storage by default and migrates existing Fen
  Light English installs to turn it on without touching TorBox authorization.
- `plugin.video.fenlight.patched.kodienglish` `2.0.71.1011`
  Patched Fen Light package carrying the recent Trakt/auth pass, stable Trakt
  list-id routing, bundled Trakt default-key refresh, and QR-based auth flows
  for Trakt, Real-Debrid, Premiumize, and AllDebrid. It now also carries the
  latest Extras trailer fallback/fullscreen-stop fixes, the duplicate Trakt
  re-authorization prompt guard, the invalid watched-indicator payload guard,
  and per-device-URL QR image filenames so Kodi refreshes changed auth codes.
  It now also refreshes the English Trakt and Real-Debrid QR-backed auth prompts
  with styled Trakt QR cards and the latest activation URL / clipboard behavior.
  It now also includes TorBox Web Download cloud support and the WebDL playback
  validation cleanup without temporary scrape/resolver diagnostics. It now also
  seeds non-secret first-run defaults for CocoScrapers, list/result/playback
  preferences, size filters, pagination, and update behavior while keeping
  KodiEnglish repository targets and local/private values clean. It now also
  adds TorBox Usenet Search controls for movies and TV shows, plus automatic
  no-results retry with cached TorBox Usenet Search, while deliberately leaving
  the normal-repo a4k subtitle-service changes out of the English build.
- `plugin.program.famyt` `0.4.2`
  Private family setup helper copied from the production release line. It
  contains no credentials; operational notes are kept outside the public
  repository.
- `plugin.program.autocompletion` `2.1.4`
  Bundled virtual keyboard autocomplete helper so Arctic Fuse 3 can install it
  from this repo instead of the broken upstream `2.1.3` package URL.
- `script.module.autocompletion` `2.1.1`
  Library dependency for the virtual keyboard autocomplete helper.
- `plugin.video.themoviedb.helper.patched.kodienglish` `6.15.2.10.1005`
  Patched TMDb Helper package used by the patched skin flow. It now includes
  the bundled Fen / Fen Patched player definitions, recommendations-window
  hardening and logging, authenticated Trakt username state, and the newer
  OMDb default-key and ratings-backfill improvements. It now also ships the
  custom Trakt QR auth dialog, styled QR generation helpers, clipboard support,
  and the matching dialog skin assets for the English repo build.
- `skin.arctic.horizon.2.patched.kodienglish` `0.8.30.12.1005`
  Patched Arctic Horizon 2 package targeting the patched TMDb Helper addon id.
  It now supports the dedicated next-episode OSD action for Fen playback and
  hides that action when Fen confirms there is no next aired episode, while
  routing the button to Fen Light English when English playback is active. It
  now also adds a Kodi/Android voice-search button to the virtual keyboard,
  uses Kodi's `VoiceRecognizer`, and auto-submits once Android voice input
  fills the keyboard text.
- `repository.kodienglish`
  The repository addon Kodi installs first.

## Layout

- `plugin.video.fenlight/`
  Vanilla Fen Light source tree kept as the baseline, with only repo-wide bundled key updates.
- `plugin.video.fenlight.kodienglish/`
  Working copy of the vanilla Fen Light source tree for English-only changes.
- `plugin.video.fenlight.patched.kodienglish/`
  Patched Fen Light source tree.
- `plugin.program.famyt/`
  Private family setup helper source. Credentials are not stored in this
  repository.
- `plugin.program.autocompletion/`
  Bundled virtual keyboard autocomplete helper source.
- `script.module.autocompletion/`
  Bundled virtual keyboard autocomplete library source.
- `plugin.video.themoviedb.helper.patched.kodienglish/`
  Patched TMDb Helper source tree.
- `skin.arctic.horizon.2.patched.kodienglish/`
  Patched Arctic Horizon 2 source tree.
- `repository.kodienglish/`
  Repository addon source generated by `scripts/build_repo.py`.
- `scripts/`
  Repo build and publish helpers.
- `zips/`
  Generated installable addon packages. Do not hand-edit these.
- `addons.xml`
  Kodi metadata for every addon in the repo.
- `addons.xml.md5`
  Checksum for `addons.xml`.

## Build And Publish

- Use `scripts/build_repo.py` when the repository addon or repo-wide metadata
  changes and you want a full rebuild.
- Use `scripts/publish_addon_update.py` when publishing an addon update without
  bumping the repository addon version.

The repository addon and metadata are published from:

- [https://github.com/TechXXX/kodienglish](https://github.com/TechXXX/kodienglish)

Kodi should consume the GitHub Pages path:

- `https://techxxx.github.io/kodienglish/`

## Generated Output Rules

- Treat `zips/` as generated output.
- If an addon `addon.xml` changes, regenerate `addons.xml`.
- Do not edit `addons.xml.md5` by hand.
- Do not ship `__pycache__` or `.pyc` files in packages.
