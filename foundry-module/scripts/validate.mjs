#!/usr/bin/env node
/**
 * Validate the CotCT conversion pack sources (Kingmaker-style structure).
 *
 *   node scripts/validate.mjs            # console report
 *   node scripts/validate.mjs --report   # also write ../reports/foundry_validation_report.md
 *
 * Checks:
 *  - every doc: 16-char _id, name, correct _key (primary + folder + adventure)
 *  - embedded actor items / journal pages: compound _key (else compile = empty/throw)
 *  - _id uniqueness per pack (the Adventure pack re-embeds cross-pack docs)
 *  - LINK RESOLUTION across the module:
 *      @UUID[Actor.<id>] / [Item.<id>] / [Scene.<id>] / [RollTable.<id>]
 *      @UUID[JournalEntry.<id>.JournalEntryPage.<id>]   (entry + page)
 *      @UUID[.<pageId>]                                 (relative, same-entry page)
 *      scene note.entryId + note.pageId
 *      scene token.actorId
 *    Compendium.pf2e.* and Compendium.cotct-* are resolved/listed.
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

const ID_RE = /^[A-Za-z0-9]{16}$/;
const COLL = { actors: "actors", hazards: "actors", items: "items", journals: "journal",
  scenes: "scenes", rolltables: "tables", macros: "macros", adventure: "adventures" };

const problems = [], info = [], stats = { packs: 0, docs: 0, pages: 0, links: 0 };
const idx = { Actor: new Set(), Item: new Set(), Scene: new Set(), JournalEntry: new Set(),
  RollTable: new Set(), Macro: new Set() };
const pagesByEntry = new Map();   // entryId -> Set(pageId)
const allPages = new Set();       // every page id (for relative links)
const COLL_TO_TYPE = { actors: "Actor", hazards: "Actor", items: "Item", journals: "JournalEntry",
  scenes: "Scene", rolltables: "RollTable", macros: "Macro" };

function walk(dir) {
  const out = [];
  for (const e of readdirSync(dir, { withFileTypes: true })) {
    const f = join(dir, e.name);
    if (e.isDirectory()) out.push(...walk(f));
    else if (e.name.endsWith(".json")) out.push(f);
  }
  return out;
}

const packDirs = existsSync(PACKS_DIR)
  ? readdirSync(PACKS_DIR).filter(p => existsSync(join(PACKS_DIR, p, "_source")) && statSync(join(PACKS_DIR, p, "_source")).isDirectory())
  : [];

// ---- index pass ----
for (const pack of packDirs) {
  stats.packs++;
  const seen = new Set();
  for (const file of walk(join(PACKS_DIR, pack, "_source"))) {
    let doc;
    try { doc = JSON.parse(readFileSync(file, "utf8")); }
    catch (err) { problems.push(`BAD JSON  ${file}: ${err.message}`); continue; }
    stats.docs++;
    const rel = file.replace(PROJECT_ROOT + "/", "");
    if (!doc._id || !ID_RE.test(doc._id)) problems.push(`MISSING/BAD _id  ${rel}`);
    if (!doc.name) problems.push(`MISSING name  ${rel}`);
    const isFolder = (doc._key || "").startsWith("!folders!");
    if (doc._id) {
      if (seen.has(doc._id)) problems.push(`DUPLICATE _id within ${pack}: ${doc._id}`);
      seen.add(doc._id);
      if (isFolder) {
        if (doc._key !== `!folders!${doc._id}`) problems.push(`BAD folder _key ${rel}`);
      } else if (COLL[pack]) {
        const ek = `!${COLL[pack]}!${doc._id}`;
        if (doc._key !== ek) problems.push(`MISSING/BAD _key ${rel} (got ${JSON.stringify(doc._key)}, expected ${ek}) — would compile EMPTY`);
        // embedded keys (NOT for the Adventure pack — its embeds are inline, no separate _key)
        if (pack !== "adventure") {
          for (const [field, ec] of [["items", "items"], ["pages", "pages"]]) {
            for (const emb of doc[field] || []) {
              const k = `!${COLL[pack]}.${ec}!${doc._id}.${emb._id}`;
              if (emb._key !== k) problems.push(`BAD embedded _key ${rel} ${field}[${emb._id}] (expected ${k})`);
            }
          }
        }
        // populate index
        const t = COLL_TO_TYPE[pack];
        if (t && idx[t]) idx[t].add(doc._id);
        if (pack === "journals") {
          const set = new Set((doc.pages || []).map(p => p._id));
          pagesByEntry.set(doc._id, set);
          for (const p of set) allPages.add(p);
          stats.pages += set.size;
        }
      }
    }
  }
}

// ---- link resolution pass ----
const UUID_RE = /@UUID\[([^\]]+)\]/g;
function resolveUuid(target, rel) {
  stats.links++;
  if (target.startsWith(".")) {                       // relative same-entry page
    const pid = target.slice(1).split("#")[0];
    if (!allPages.has(pid)) problems.push(`BROKEN relative page link ${rel}: @UUID[${target}]`);
    return;
  }
  if (target.startsWith("Compendium.")) {
    if (!target.startsWith(`Compendium.${MODULE_ID}.`)) info.push(`external ${target.split(".").slice(0,3).join(".")}  (${rel})`);
    return;
  }
  const parts = target.split(".");
  const [type, id] = parts;
  if (type === "JournalEntry" && parts[2] === "JournalEntryPage") {
    if (!idx.JournalEntry.has(id)) problems.push(`BROKEN ${rel}: JournalEntry.${id} not found`);
    else if (!(pagesByEntry.get(id) || new Set()).has(parts[3])) problems.push(`BROKEN ${rel}: page ${parts[3]} not in entry ${id}`);
    return;
  }
  if (idx[type]) {
    if (!idx[type].has(id)) problems.push(`BROKEN ${rel}: ${type}.${id} not found`);
  } // unknown types (Actor.Item nested etc.) skipped
}

for (const pack of packDirs) {
  for (const file of walk(join(PACKS_DIR, pack, "_source"))) {
    let raw, doc;
    try { raw = readFileSync(file, "utf8"); doc = JSON.parse(raw); } catch { continue; }
    const rel = file.replace(PROJECT_ROOT + "/", "");
    if (pack === "adventure") continue; // embedded copies; canonical checked in their own packs
    let m; while ((m = UUID_RE.exec(raw)) !== null) resolveUuid(m[1], rel);
    // scene note + token links
    for (const n of doc.notes || []) {
      if (n.entryId && !idx.JournalEntry.has(n.entryId)) problems.push(`BROKEN note ${rel}: entryId ${n.entryId} not found`);
      if (n.entryId && n.pageId && !(pagesByEntry.get(n.entryId) || new Set()).has(n.pageId)) problems.push(`BROKEN note ${rel}: pageId ${n.pageId} not in entry ${n.entryId}`);
    }
    for (const t of doc.tokens || []) {
      if (t.actorId && !idx.Actor.has(t.actorId)) problems.push(`BROKEN token ${rel}: actorId ${t.actorId} not found`);
    }
  }
}

// ---- report ----
const lines = [], log = s => { lines.push(s); console.log(s); };
log(`# Foundry validation`);
log(`packs=${stats.packs} docs=${stats.docs} pages=${stats.pages} links=${stats.links} problems=${problems.length}`);
log("");
log("## Problems");
if (problems.length) for (const p of problems) log(`- ${p}`); else log("- none ✅");
const ext = [...new Set(info)];
if (ext.length) { log(`\n## External compendium refs (${ext.length} unique)`); for (const e of ext.slice(0, 60)) log(`- ${e}`); }

if (writeReport) {
  const dir = join(PROJECT_ROOT, "reports"); mkdirSync(dir, { recursive: true });
  writeFileSync(join(dir, "foundry_validation_report.md"),
    `# Foundry Validation Report\n\n_Generated by scripts/validate.mjs (deterministic)._\n\n` + lines.join("\n") + "\n");
  console.log("\nwrote reports/foundry_validation_report.md");
}
process.exit(problems.length ? 1 : 0);
