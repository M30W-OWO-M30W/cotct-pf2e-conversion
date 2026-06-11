// Extract scene geometry (walls, doors, tiles, dims) from the locally installed
// "Racooze's Curse of the Crimson Throne Battlemaps" module so the build can
// inject it into our prepared scenes. Same firewall pattern as the AP.md
// read-aloud injection: Racooze's data and images are NEVER committed — the
// output JSON is gitignored, and the build falls back to placeholder scenes
// when it is absent.
// Run: node scripts/extract_racooze.mjs   (writes scripts/racooze_scenes.json)
import { ClassicLevel } from "classic-level";
import { writeFileSync, existsSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const HERE = dirname(fileURLToPath(import.meta.url));
const MOD = "/mnt/c/Users/maman/AppData/Local/FoundryVTT/Data/modules/racoozes-curse-of-the-crimson-throne-battlemaps";
const PACK = join(MOD, "packs/racoozes-curse-of-the-crimson-throne-battlemaps");

if (!existsSync(PACK)) {
  console.log("[extract_racooze] Racooze battlemaps module not installed — skipping (scenes build as placeholders).");
  process.exit(0);
}

// LevelDB stores embedded collections under separate keys
// (!scenes.walls!<sceneId>.<id>) with the parent holding id strings — reassemble.
const parents = {}, embeds = {};
const db = new ClassicLevel(PACK, { valueEncoding: "json" });
for await (const [key, doc] of db.iterator()) {
  if (key.startsWith("!scenes!")) { parents[doc._id] = doc; continue; }
  const m = key.match(/^!scenes\.(walls|tiles|lights)!([^.]+)\./);
  if (m) ((embeds[m[2]] ??= { walls: [], tiles: [], lights: [] })[m[1]]).push(doc);
}
await db.close();
const scenes = {};
let n = 0;
for (const doc of Object.values(parents)) {
  const e = embeds[doc._id] ?? { walls: [], tiles: [], lights: [] };
  scenes[doc.name] = {
    name: doc.name, width: doc.width, height: doc.height, padding: doc.padding,
    grid: doc.grid, walls: e.walls, tiles: e.tiles, lights: e.lights,
    thumb: doc.thumb ?? null,    // his pre-rendered sidebar thumbnail
  };
  n++;
}
writeFileSync(join(HERE, "racooze_scenes.json"), JSON.stringify(scenes));
console.log(`[extract_racooze] ${n} scenes -> scripts/racooze_scenes.json`);
