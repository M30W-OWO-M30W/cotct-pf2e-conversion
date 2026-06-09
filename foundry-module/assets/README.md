# Assets

Drop table assets into these folders before using the scene placeholders:

- `maps/`   — battle/region maps (one image per scene)
- `tokens/` — creature/NPC token art
- `art/`    — handouts, NPC portraits

Each scene-planning journal lists which map image it expects and the suggested
grid dimensions. File names referenced by scene records use the convention
`maps/<chapter>-<area-slug>.webp`.

Binary image files in this tree are git-ignored (see repo `.gitignore`); only
`.md`/`.txt` notes and `.gitkeep` files are committed.
