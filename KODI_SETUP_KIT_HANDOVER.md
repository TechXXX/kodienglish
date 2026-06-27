# Kodi Setup Kit Handover For KodiEnglish

Last updated: 2026-06-27.

This repo carries the English-feed copy of `plugin.program.famyt`, user-facing
as **Kodi Setup Kit**. The canonical long-form Setup Kit runbook is in the main
repo:

`/Users/kalter/Documents/CODEX/kodirepo/KODI_SETUP_KIT_HANDOVER.md`

Read that document before changing the installer, presets, Vercel bridge
contract, or `Install everything` order. The same concepts apply here:

- no private credentials in this repo
- Vercel is the private credential source
- top-level `[ALL]` items are the curated `Install everything` flow
- Fen Light settings must be restored before TorBox credentials
- a4kSubtitles preset must be restored before a4kSubtitles credentials
- GUI webserver credentials come from Vercel, not the bundled GUI preset
- missing optional add-ons should skip cleanly instead of aborting the whole
  setup run

Current Setup Kit version at this handover: `0.9.15`.

## KodiEnglish-Specific Notes

The Setup Kit source should usually match the main repo, but this repository
has its own packaging context:

- preserve KodiEnglish `addon.xml` dependency differences
- keep the KodiEnglish handover guardrail against subtitle selector work
- do not import normal-repo a4k selector stack changes into the brother addon
  unless the user explicitly asks for that in the same conversation
- regenerate `addons.xml`, `addons.xml.md5`, and `addons.xml.md5.txt` when
  publishing a Kodi-visible Setup Kit update

## Quick Publish Reminder

For a Setup Kit release in this repo:

1. Sync the intended shared files from `kodirepo/plugin.program.famyt`.
2. Patch KodiEnglish-specific metadata by hand if needed.
3. Bump `plugin.program.famyt/addon.xml`.
4. Rebuild `zips/plugin.program.famyt/` and the zip archive.
5. Regenerate `addons.xml`, `addons.xml.md5`, and `addons.xml.md5.txt`.
6. Run `py_compile`, XML parse checks, zip hygiene checks, and source/mirror
   parity checks.
7. Commit and push `main`.

For the full component-by-component behavior, Vercel env vars, live paths,
and troubleshooting notes, use the main repo handover document.
