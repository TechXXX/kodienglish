# Kodi English Repository

This repository is a GitHub Pages Kodi add-on feed focused on the English
packages copied from the Dutch release line.

This repo keeps one untouched vanilla Fen Light copy under the original
`plugin.video.fenlight` ID as a known-good baseline, and uses the
`.kodienglish` suffix for the English working copy and the other forked add-ons.

## Brother Target Addon

The user's brother uses:

`plugin.video.fenlight.kodienglish`

That addon is the English-speaker Fen Light working copy. Keep it simpler than
the patched selector stack:

- do not port subtitle-selector architecture into it
- do not add `resources/lib/fenlightsubs/` selector behavior
- do not wire it into patched a4k subtitle-selector integration
- keep English-focused fixes and repo maintenance flowing there when asked
- IntroDB support is wanted for this addon; it is the explicit exception to the
  "no selector stack" simplification

## Maintenance Guardrail

Do not port, cherry-pick, test, or publish subtitle selector work into this
KodiEnglish repository. That includes changes from `TechXXX/kodirepo`,
`TechXXX/DutchTechTestRepo`, or any other branch/repo touching bundled selector
logic, a4k subtitle selector integration, subtitle-backed autoplay retry
ranking, `resources/lib/fenlightsubs/`, or matching mirrored files under
`zips/`.

If a requested change touches subtitle selector code or a4k subtitle integration,
stop and ask before editing. KodiEnglish should keep only explicitly requested
English repo fixes such as Fen/TorBox/famYT work, dependency recovery, or skin
repo maintenance.

## Addons In This Repo

Current source-tree versions:

- `plugin.video.fenlight` `2.0.16.1004`
  Vanilla Fen Light package kept as the known-good baseline with repo-wide bundled key updates plus TorBox Web Download cloud support.
- `plugin.video.fenlight.kodienglish` `2.0.16.1026`
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
  It now also applies the curated Magneto provider selection automatically when
  the Magneto migration path runs.
  It should stay free of the subtitle-selector/a4k patched stack. It now includes
  TheIntroDB support with the shipped default API key, English skip intro/recap
  buttons, and next-episode timing support for episode playback. It now also
  tracks Trakt's 2026 watched endpoint change by requesting TV watched data
  with `extended=progress`, guarding missing `seasons` payloads, and running a
  one-time empty episode-watched cache repair after update.
- `script.module.magneto` `6.07.04`
  Magnet provider aggregation module carried directly in KodiEnglish so Fen
  Light English installs can resolve the dependency and use the same curated
  defaults as the main repo feed.
- `plugin.program.famyt` `0.9.22`
  Kodi Setup Kit, the private family bootstrap helper copied from the
  production release line. It contains no credentials; the matching Vercel
  bridge supplies YouTube, TorBox, a4kSubtitles, and Kodi webserver secrets
  after the shared password is provided. It now also merges bundled default
  favourites into the live Kodi profile with a backup-first restore path and
  includes that step in Install everything. Read `KODI_SETUP_KIT_HANDOVER.md`
  before changing its install flow.
- `plugin.program.autocompletion` `2.1.4`
  Bundled virtual keyboard autocomplete helper so Kodi English Fuse 3 can pull
  the dependency from this repo instead of the broken upstream `2.1.3` package
  URL.
- `resource.images.studios.coloured` `0.0.25`
  Coloured studio-logo resource used by the Kodi English skins. This build is
  based on the official `0.0.24` texture bundle and adds a plain Apple TV
  studio icon entry (`Apple TV.png`) generated from Fen Light's provider
  artwork, keeping it aligned with the main DutchTech repo resource.
- `script.module.autocompletion` `2.1.1`
  Library dependency for the virtual keyboard autocomplete helper.
- `script.fenlight.quickrescrape.kodienglish` `0.0.4.1002`
  Shield/Android shortcut helper for the English repo. It installs a
  KodiEnglish-specific keymap and opens Fen Light English source-select/rescrape
  for the focused AH2 movie or episode item.
- `plugin.video.themoviedb.helper.patched.kodienglish` `6.15.2.12.1009`
  Patched TMDb Helper package used by the patched skin flow. It now includes
  the bundled Fen / Fen Patched player definitions, recommendations-window
  hardening and logging, authenticated Trakt username state, and the newer
  OMDb default-key and ratings-backfill improvements. It now also ships the
  custom Trakt QR auth dialog, styled QR generation helpers, clipboard support,
  and the matching dialog skin assets for the English repo build.
- `skin.arctic.horizon.2.patched.kodienglish` `0.8.30.13.1007`
  Patched Arctic Horizon 2 package targeting the patched TMDb Helper addon id.
  It now supports the dedicated next-episode OSD action for Fen playback and
  hides that action when Fen confirms there is no next aired episode, while
  routing the button to Fen Light English when English playback is active.
- `skin.dutchtech.fuse.3.kodienglish` `3.2.9.1013`
  Kodi English fork of the latest Arctic Fuse 3 `v3.2.9` release with a
  separate addon id and KodiEnglish patched TMDb Helper routing. It is now
  kept intentionally in lockstep with `/Users/kalter/Documents/CODEX/kodirepo/skin.dutchtech.fuse.3`,
  with only the KodiEnglish addon identity and plugin target ids diverging.
  Its non-core dependencies are all carried by this repo: Skin Variables,
  Texture Maker, the KodiEnglish patched TMDb Helper, weather icons, studio
  icons, the Roboto CJK font resource, and the bundled virtual keyboard
  autocomplete helper. It now also keeps category selector labels static when
  unfocused and scrolls only the focused row.
- `repository.kodienglish`
  The repository addon Kodi installs first.

## Layout

- `plugin.video.fenlight/`
  Vanilla Fen Light source tree kept as the baseline, with only repo-wide bundled key updates.
- `plugin.video.fenlight.kodienglish/`
  Working copy of the vanilla Fen Light source tree for English-only changes.
- `plugin.program.famyt/`
  Kodi Setup Kit source. Credentials are not stored in this repository; the
  matching Vercel bridge is documented in `KODI_SETUP_KIT_HANDOVER.md`.
- `plugin.program.autocompletion/`
  Virtual keyboard autocomplete helper source.
- `resource.images.studios.coloured/`
  Coloured studio-logo image resource, including the Apple TV studio-icon
  source PNG and patched texture bundle.
- `script.module.autocompletion/`
  Virtual keyboard autocomplete library source.
- `script.module.magneto/`
  Magneto module source.
- `script.fenlight.quickrescrape.kodienglish/`
  English Quick Rescrape helper source and package artwork.
- `plugin.video.themoviedb.helper.patched.kodienglish/`
  Patched TMDb Helper source tree.
- `skin.arctic.horizon.2.patched.kodienglish/`
  Patched Arctic Horizon 2 source tree.
- `skin.dutchtech.fuse.3.kodienglish/`
  Kodi English Fuse 3 source forked from Arctic Fuse 3.
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
- Before publishing any Kodi-visible addon change, bump the affected addon's
  `addon.xml` version to a number strictly higher than the version already
  advertised in `addons.xml`; replacing a same-version zip is not an update.

The repository addon and metadata are published from:

- [https://github.com/TechXXX/kodienglish](https://github.com/TechXXX/kodienglish)

Kodi should consume the GitHub Pages path:

- `https://techxxx.github.io/kodienglish/`

## Generated Output Rules

- Treat `zips/` as generated output.
- Keep only the package zip for each addon's currently advertised version;
  unreferenced old zips can push the GitHub Pages artifact over the deploy
  limit.
- If an addon `addon.xml` changes, regenerate `addons.xml`.
- Do not edit `addons.xml.md5` by hand.
- Do not ship `__pycache__` or `.pyc` files in packages.
