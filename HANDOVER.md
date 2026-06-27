# KodiEnglish Handover

## Hard Guardrail

Do not put new subtitle selector work in this repository.

Subtitle selector and a4k subtitle integration changes belong in the normal/test
repos, not in KodiEnglish. In particular, do not port or cherry-pick commits
from `TechXXX/kodirepo` or `TechXXX/DutchTechTestRepo` when they touch:

- `resources/lib/fenlightsubs/`
- subtitle selector ranking or normalization
- a4k subtitle selector/runtime handoff code
- subtitle-backed autoplay retry logic
- selector shadow-validation or subtitle trace files
- matching generated copies under `zips/`

If any task asks for subtitle selector changes in KodiEnglish, stop and ask for
confirmation before editing. Do not infer permission from a request to update
Fen Light, Fen Light Patched, subtitles, a4k, or repo packages.

## Allowed Work

KodiEnglish work should stay limited to explicitly requested English repo
maintenance, for example:

- Fen/TorBox settings and cloud/usenet behavior requested for the English repo
- famYT public metadata or installer maintenance
- dependency recovery packages needed to repair Kodi installs
- skin/repository packaging fixes requested specifically for KodiEnglish

Before any publish, verify `git diff --name-only` does not include new selector
or a4k subtitle integration paths unless the user explicitly overrode this
handover in the same conversation.

## Kodi Setup Kit / famYT

`plugin.program.famyt` is now user-facing as Kodi Setup Kit. For installer
changes, read `KODI_SETUP_KIT_HANDOVER.md` in this repo and the full canonical
runbook at `/Users/kalter/Documents/CODEX/kodirepo/KODI_SETUP_KIT_HANDOVER.md`.

Keep the Setup Kit behavior aligned with the main repo unless the user asks
for an English-specific difference. Do not store credentials here; the matching
Vercel bridge supplies private values after the shared family password is
provided.
