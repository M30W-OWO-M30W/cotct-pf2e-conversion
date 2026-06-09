#!/usr/bin/env node
/**
 * Validate the JSON pack sources for the CotCT PF2e conversion module.
 *
 *   node scripts/validate.mjs            # console report
 *   node scripts/validate.mjs --report   # also write ../../reports/foundry_validation_report.md
 *
 * Checks:
 *  - every document has a 16-char alphanumeric _id and a name
 *  - _id uniqueness within each pack AND globally
 *  - declared module/packs in module.json match the packs on disk
 *  - every @UUID[...] and Compendium.<...> link that points INTO this module
 *    resolves to a document/page that exists
 *  - reports external compendium refs (pf2e.* etc.) as informational
 *
 * Pure read-only; deterministic ordering.
 */
import { readdirSync, existsSync, statSync, readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join, resolve } from "node:path";

const __dirname = dirname(fileURLToPath(import.meta.url));
const MODULE_ROOT = resolve(__dirname, "..");
const PROJECT_ROOT = resolve(MODULE_ROOT, "..");
const PACKS_DIR = join(MODULE_ROOT, "packs");
const MODULE_ID = "cotct-pf2e-conversion";
const writeReport = process.argv.includes("--report");

const moduleJson = JSON.parse(readFileSync(join(MODULE_ROOT, "module.json"), "utf8"));
const declaredPacks = new Map(moduleJson.packs.map((p) => [p.name, p]));

const ID_RE = /^[A-Za-z0-9]{16}$/;
const problems = [];
const info = [];
const docIndex = new Map(); // "<packName>.<_id>" -> {name, type, pages:Set}
const globalIds = new Map(); // _id -> packName (first seen)
const stats = { packs: 0, docs: 0, pages: 0 };

function walkJson(dir) {
  const out = [];
  for (const e of readdirSync(dir, { withFileTypes: true })) {
    const full = join(dir, e.name);
    if (e.isDirectory()) out.push(...walkJson(full));
    else if (e.name.endsWith(".json")) out.push(full);
  }
  return out;
}

// ---- index pass ----
const packDirs = existsSync(PACKS_DIR)
  ? readdirSync(PACKS_DIR).filter((p) => existsSync(join(PACKS_DIR, p, "_source")) && statSync(join(PACKS_DIR, p, "_source")).isDirectory())
  : [];

for (const pack of packDirs) {
  stats.packs++;
  if (!declaredPacks.has(`${MODULE_ID === MODULE_ID ? "" : ""}cotct-${pack}`) && !declaredPacks.has(`cotct-${pack}`)) {
    // pack dirs are named e.g. "journals" -> declared name "cotct-journals"
    if (!declaredPacks.has(`cotct-${pack}`)) info.push(`pack dir '${pack}' not declared in module.json (expected name 'cotct-${pack}')`);
  }
  const files = walkJson(join(PACKS_DIR, pack, "_source"));
  for (const file of files) {
    let doc;
    try { doc = JSON.parse(readFileSync(file, "utf8")); }
    catch (err) { problems.push(`BAD JSON  ${file}: ${err.message}`); continue; }
    stats.docs++;
    const rel = file.replace(PROJECT_ROOT + "/", "");
    if (!doc._id || !ID_RE.test(doc._id)) problems.push(`MISSING/BAD _id  ${rel} (got ${JSON.stringify(doc._id)})`);
    if (!doc.name) problems.push(`MISSING name  ${rel}`);
    // _key is REQUIRED by the fvtt compiler (docs without it are silently skipped -> empty packs)
    const COLL = { actors: "actors", hazards: "actors", items: "items", journals: "journal", rolltables: "tables", macros: "macros", scenes: "scenes" };
    if (doc._id && COLL[pack]) {
      const expectedKey = `!${COLL[pack]}!${doc._id}`;
      if (doc._key !== expectedKey) problems.push(`MISSING/BAD _key  ${rel} (got ${JSON.stringify(doc._key)}, expected ${expectedKey}) — pack would compile EMPTY`);
      // embedded docs (actor items, journal pages) need compound keys or compile throws LEVEL_INVALID_KEY
      const embChecks = [["items", "items"], ["pages", "pages"]];
      for (const [field, embColl] of embChecks) {
        for (const emb of doc[field] || []) {
          const ek = `!${COLL[pack]}.${embColl}!${doc._id}.${emb._id}`;
          if (emb._key !== ek) problems.push(`BAD embedded _key  ${rel} ${field}[${emb._id || "?"}] (expected ${ek})`);
        }
      }
    }
    if (doc._id) {
      const key = `cotct-${pack}.${doc._id}`;
      docIndex.set(key, { name: doc.name, type: doc.type, pages: new Set((doc.pages || []).map((pg) => pg._id)) });
      stats.pages += (doc.pages || []).length;
      if (globalIds.has(doc._id)) problems.push(`DUPLICATE _id  ${doc._id}  in cotct-${pack} and ${globalIds.get(doc._id)}`);
      else globalIds.set(doc._id, `cotct-${pack}`);
    }
  }
}

// ---- link pass ----
const UUID_RE = /(?:@UUID\[)?Compendium\.([\w-]+)\.([\w-]+)\.(?:(\w+)\.)?([A-Za-z0-9]{16})(?:\.JournalEntryPage\.([A-Za-z0-9]{16}))?/g;
for (const pack of packDirs) {
  for (const file of walkJson(join(PACKS_DIR, pack, "_source"))) {
    let raw;
    try { raw = readFileSync(file, "utf8"); } catch { continue; }
    const rel = file.replace(PROJECT_ROOT + "/", "");
    let m;
    while ((m = UUID_RE.exec(raw)) !== null) {
      const [, mod, packName, , docId, pageId] = m;
      if (mod !== MODULE_ID) { info.push(`external ref ${mod}.${packName} in ${rel}`); continue; }
      const key = `${packName}.${docId}`;
      const target = docIndex.get(key);
      if (!target) { problems.push(`BROKEN LINK  ${rel} -> Compendium.${mod}.${packName}.*.${docId} (not found)`); continue; }
      if (pageId && !target.pages.has(pageId)) problems.push(`BROKEN PAGE LINK  ${rel} -> page ${pageId} in ${target.name}`);
    }
  }
}

// ---- report ----
const lines = [];
const log = (s) => { lines.push(s); console.log(s); };
log(`# Foundry validation`);
log(`packs(dirs)=${stats.packs} docs=${stats.docs} pages=${stats.pages} problems=${problems.length} info=${info.length}`);
log("");
if (problems.length) { log("## Problems"); for (const p of problems) log(`- ${p}`); }
else log("## Problems\n- none ✅");
const extRefs = [...new Set(info.filter((i) => i.startsWith("external ref")))];
if (extRefs.length) { log("\n## External compendium refs (informational)"); for (const e of extRefs.slice(0, 200)) log(`- ${e}`); }

if (writeReport) {
  const reportsDir = join(PROJECT_ROOT, "reports");
  mkdirSync(reportsDir, { recursive: true });
  writeFileSync(join(reportsDir, "foundry_validation_report.md"),
    `# Foundry Validation Report\n\n_Generated by scripts/validate.mjs (deterministic)._\n\n` + lines.join("\n") + "\n");
  console.log(`\nwrote reports/foundry_validation_report.md`);
}
process.exit(problems.length ? 1 : 0);
