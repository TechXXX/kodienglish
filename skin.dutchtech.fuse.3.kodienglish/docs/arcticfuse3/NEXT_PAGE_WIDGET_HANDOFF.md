# AF3 Next-Page Widget Handoff

KodiEnglish uses the same AF3 next-page widget behavior as the main DutchTech
skin fork in:

- `/Users/kalter/Documents/CODEX/kodirepo/skin.dutchtech.fuse.3`

Do not maintain a separate KodiEnglish-only next-page implementation here. When
the DutchTech fork changes next-page behavior, resync the KodiEnglish skin tree
and then reapply the KodiEnglish package identity and plugin target rewrites.

KodiEnglish-specific route targets that must remain preserved after sync:

- `skin.dutchtech.fuse.3.kodienglish`
- `plugin.video.themoviedb.helper.patched.kodienglish`
- `plugin.video.fenlight.kodienglish`
