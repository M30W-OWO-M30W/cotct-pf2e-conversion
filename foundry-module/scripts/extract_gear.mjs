// Append real pf2e equipment templates (by slug) into scripts/srd_gear.json,
// matching the existing template shape (name/type/img/system, description stubbed
// to the SRD @UUID link, _id/_key stripped — gear() fills _id/qty at build).
// Usage: node scripts/extract_gear.mjs club steel-shield longsword rapier
import { ClassicLevel } from "classic-level";
import { readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const PF = "/mnt/c/Users/maman/AppData/Local/FoundryVTT/Data/systems/pf2e/packs/equipment";
const want = new Set(process.argv.slice(2));
const out = JSON.parse(readFileSync(join(import.meta.dirname, "srd_gear.json"), "utf-8"));

const db = new ClassicLevel(PF, { valueEncoding: "json" });
const found = new Set();
for await (const [key, doc] of db.iterator()) {
  const slug = doc?.system?.slug || doc?.name?.toLowerCase().replace(/[^a-z0-9]+/g, "-");
  if (!want.has(slug) || found.has(slug)) continue;
  found.add(slug);
  const sys = doc.system;
  sys.description = { value: `<p>@UUID[Compendium.pf2e.equipment-srd.Item.${doc._id}]</p>`, gm: "" };
  sys.quantity = 1;
  out[slug] = { name: doc.name, type: doc.type, img: doc.img, system: sys };
}
await db.close();
const sorted = {};
for (const k of Object.keys(out).sort()) sorted[k] = out[k];
writeFileSync(join(import.meta.dirname, "srd_gear.json"), JSON.stringify(sorted, null, 2));
console.log("added:", [...found].join(", ") || "(none)", "| missing:", [...want].filter(s => !found.has(s)).join(", ") || "(none)");
