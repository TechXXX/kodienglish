# Kodi English Repo Scripts

This directory contains the helper scripts that build and publish the
`KodiEnglish` Kodi repository.

## `build_repo.py`

Use this when the repository addon or the repo-wide metadata needs a full
rebuild.

What it does:

- ensures the repository addon source exists
- bumps the repository addon version
- rebuilds every addon package under `zips/`
- regenerates `addons.xml` and `addons.xml.md5`
- updates the repository install zip in the repo root
- commits and pushes to `main`

## `publish_addon_update.py`

Use this for addon updates when you do not want to bump the repository addon
version.

The command-line script expects the classic workflow:

1. put a packaged addon zip in the repo root
2. run the script

What it does:

- imports the root zip into the matching source directory
- rebuilds the matching `zips/<addon-id>/` output
- regenerates `addons.xml` and `addons.xml.md5`
- commits and pushes to `main`

## Generated Files

Never hand-edit:

- `zips/`
- `addons.xml`
- `addons.xml.md5`
