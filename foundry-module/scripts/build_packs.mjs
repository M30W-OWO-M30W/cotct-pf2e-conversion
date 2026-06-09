#!/usr/bin/env node
/**
 * Compile JSON pack sources -> Foundry LevelDB packs (and back).
 *
 *   node scripts/build_packs.mjs            # compile every packs/<p>/_source -> packs/<p>
 *   node scripts/build_packs.mjs --extract  # extract packs/<p> (leveldb) -> _source JSON
 *
 * Requires the Foundry CLI lib:  npm install   (declared in package.json)
 * Docs: https://github.com/foundryvtt/foundryvtt-cli
 *
 * We version the human-readable _source/*.json (one document per file) and treat
 * the compiled LevelDB as a build artifact (git-ignored). This keeps diffs
 * reviewable and the repo free of binary blobs.
 */
import { readdirSync, existsSync, statSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join, resolve } from "node:path";

const __dirname = dirname(fileURLToPath(import.meta.url));
const MODULE_ROOT = resolve(__dirname, "..");
const PACKS_DIR = join(MODULE_ROOT, "packs");
const extract = process.argv.includes("--extract");

let compilePack, extractPack;
try {
  ({ compilePack, extractPack } = await import("@foundryvtt/foundryvtt-cli"));
} catch {
  console.error("\n  @foundryvtt/foundryvtt-cli not installed.");
  console.error("  Run:  cd foundry-module && npm install\n");
  process.exit(1);
}

const packs = readdirSync(PACKS_DIR).filter((p) => {
  const src = join(PACKS_DIR, p, "_source");
  return existsSync(src) && statSync(src).isDirectory();
});

if (!packs.length) {
  console.log("No packs with a _source/ directory found — nothing to do yet.");
  process.exit(0);
}

for (const p of packs) {
  const dest = join(PACKS_DIR, p);
  const src = join(dest, "_source");
  const hasJson = readdirSync(src).some((f) => f.endsWith(".json"));
  if (extract) {
    console.log(`extract  ${p}  (leveldb -> _source json)`);
    await extractPack(dest, src, { yaml: false, log: false });
  } else if (hasJson) {
    console.log(`compile  ${p}  (_source json -> leveldb)`);
    await compilePack(src, dest, { yaml: false, log: false, recursive: true });
  } else {
    console.log(`skip     ${p}  (no json sources yet)`);
  }
}
console.log("done.");
