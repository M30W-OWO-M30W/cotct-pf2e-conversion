# Conversion Audit — Curse of the Crimson Throne (PF1e → PF2e)

_Phase 1 deliverable. Built from the source PDF (full text extraction, page-tagged)
and the Phase-1 research sweep. Companion docs: [`PROJECT_PLAN.md`](PROJECT_PLAN.md),
[`research/research_index.md`](research/research_index.md),
[`conversion_change_log.md`](conversion_change_log.md). Per-chapter raw inventories
live in `.work/digest_maps/` (git-ignored)._

Copyright note: this audit uses **summaries + page citations only** (PDF page =
printed page; verified offset 0). No AP prose is reproduced.

---

## 1. AP identification

| Field | Value |
|---|---|
| Adventure Path | **Curse of the Crimson Throne** |
| Edition / printing | PFRPG (PF1e) **Anniversary Edition** single hardcover, © 2016 Paizo Inc. (compiles the 2008 3.5 six-volume run, with fixes) |
| Source file | `…/Curse of the Crimson Throne AP.pdf`, 482 pp, 52 MB |
| Setting | **Korvosa**, Varisia, Golarion (urban-led, then Cinderlands → Belkzen → Mushfens) |
| Structure | Introduction + **6 chapters** + Appendices 1–7 |
| PF1e level span | **1 → ~17** |
| PF1e party assumptions | 4 PCs, 15-pt buy, PF1e wealth-by-level, campaign traits tying each PC to Gaedren Lamm; deep splatbook dependency (Bestiary 1–5, NPC Codex, Ultimate Intrigue, GMG) |
| **PF2e target assumptions** | **4 PCs**, Remaster (Player Core/GM Core/Monster Core), **milestone leveling** with per-chapter advancement track, no Free Archetype/ABP (default — confirm); encounter math to PF2e XP budgets; treasure rebuilt to PF2e Treasure-by-Level |

There is **no official PF2e version** of this AP; all PF2e versions are community work (see research §B). Our source is the same Anniversary Edition the leading community conversion (Olliebird) targets, so area codes/page refs line up.

### Chapter overview & target levels

| # | Chapter | PDF pp. | PF1e lvls | PF2e target | Set-piece / climax |
|---|---------|---------|-----------|-------------|--------------------|
| Intro | — | 4–9 | — | — | Campaign traits, Harrow char-gen, synopsis |
| 1 | **Edge of Anarchy** | 10–67 | 1–4 | **1→4** | Gaedren Lamm @ Old Fishery; Dead Warrens (Vreeg); Trinia's execution / Blackjack |
| 2 | **Seven Days to the Grave** | 68–131 | 4–7 | **4→7** | Blood Veil plague; Hospice/Temple of Urgathoa; Lady Andaisin |
| 3 | **Escape from Old Korvosa** | 132–189 | 7–9 | **7→9** | Pilts Swastel; Arkona rakshasas; the Vivified Labyrinth |
| 4 | **A History of Ashes** | 190–255 | 9–11 | **9→11/12** | Cinderlands; Respect quests; Flameford Assault; Deathhead Vault |
| 5 | **Skeletons of Scarwall** | 256–331 | 11–14 | **11→14/15** | Castle Scarwall; 4 spirit anchors + Mithrodar; recover **Serithtial** |
| 6 | **Crown of Fangs** | 332–391 | 14–16 | **14→17** | Castle Korvosa (Infiltration); Sunken Queen; **Ileosa** + Kazavon fail-state |
| App | 1–7 | 392–482 | — | — | Korvosa gazetteer, **Harrow subsystem (54 cards)**, Blood Veil rules, artifacts, NPC Codex (12 blocks), Bestiary (9 monsters + 8 tables) |

---

## 2. File inventory

| Expected input | Status | Detail |
|---|---|---|
| PF1e AP PDF | ✅ found | The 482-pp Anniversary hardcover (above). Extracted to page-tagged chapter files. |
| Community conversion docs | ✅ via research | GM provided the Reddit thread → **Olliebird's 7-Google-Doc conversion** (primary). Also: paid Pathfinder Infinite guide, stale GitHub repo, forum/blog balance & QoL corpus. All catalogued in `research/research_index.md`. None stored locally (copyright). |
| Foundry world/module for this AP | ❌ none | No existing CotCT Foundry module. **Racooze's CotCT Battlemaps** (Foundry, free, Community Use) adopted as a soft map dependency. The unrelated "Ma'at" module exists but is a tool, not a conversion. |
| Foundry / PF2e versions | ✅ confirmed | Foundry **v13** (build 351), PF2e **7.12.2** (Remaster). |
| Output location | ✅ | `/home/saber/pf2e-conversion/curse-of-the-crimson-throne/` (private git repo). |
| **Missing / to confirm** | ⚠️ | GM decisions G-Q1…G-Q6 in research §H (level cap, which Olliebird artifact, telegraph vs mystery, plague structure, maps dependency, Harrow reroll style). None block the pilot. |

---

## 3. Content map

Totals across the AP (from structured extraction): **~237 keyed encounters, ~225 NPC/creature entries, ~94 hazards/traps/haunts, ~61 afflictions, subsystems in every chapter.** Per-chapter detail below; exhaustive lists in `.work/digest_maps/`.

### 3.1 Major recurring NPCs (cross-chapter — build once, reuse)

These need consistent PF2e builds across chapters; appendix stat-block pages noted.

| NPC | Role | PF1e (CR / class) | Appx p. | Notes |
|---|---|---|---|---|
| **Queen Ileosa Arabasti** | BBEG | CR 21, aristocrat 2/**bard 18**, erinyes-bound, regen 20 (only Serithtial bypasses) | 444 | Final boss Ch6; off-stage driver Ch1–5 |
| **Kazavon** | ancient **blue** dragon; Crown of Fangs source; CR-25 fail-state | CR 25 great wyrm blue | 448 | "Rise of the Dragon" conclusion only |
| **Sabina Merrin** | Gray Maiden commander; redeemable | CR 14, fighter 14 | 454 | Defects Ch6 (Zarmangarof set-piece) |
| **Cressida Kroft** | Korvosan Guard Field Marshal; patron | CR 9, aristocrat 1/fighter 9 | 442 | Quest-giver Ch1–6 |
| **Vencarlo Orisini / Blackjack** | swordmaster vigilante; mantle to a PC | CR 10, **vigilante 10** | 462 | **No PF2e vigilante class** → rebuild |
| **Zellara** | harrow-spirit guide / intelligent deck | spirit (Ego 8) | 437 | Powers the Harrow subsystem all AP |
| **Laori Vaus** | cheery Zon-Kuthon cleric; Ch5 Ally/Enemy | CR 10, cleric 11 | 450 | Recurs Ch3→Ch5 |
| **Shadowcount Sial** (+ eidolon **Asyra**) | Brotherhood of Bones; Ch5 Ally/Enemy | CR 11, **unchained summoner 12** | 456 | **No PF2e summoner-eidolon parity** → rebuild as creature |
| **Rolth Lamm** | necromancer, Gaedren's son, "Key-Lock Killer" | CR 8, rogue 1/necromancer 8 | 452 | Ch1 (offstage)→Ch2 boss |
| **Thousand Bones** | Shoanti shaman patron | CR 7, shaman 8 | 458 | Ch1 quest, Ch4 patron |
| **Trinia Sabor** | framed painter; ally | CR 4 (→CR 8 advanced) | 460 | Ch1 chase → Ch2/4 ally |
| **Bahor / Glorio Arkona** | rakshasa patriarch; Cerulean Society | CR 14, rakshasa rogue 8 | 440 | Ch1 seeds → Ch3 |
| Neolandus, Grau Soldado, Ishani Dhatri, Krojun, Cinnabar, Koriantu, Kayltanya, Togomor, Marcus Endrin | various allies/villains | see chapters | 446, 81, etc. | Mid-tier recurring |

### 3.2 Per-chapter content map

**Ch1 — Edge of Anarchy** (57 loc / 39 NPC / 37 enc / 15 haz / 9 affl / 8 subsys)
- *Dungeons:* Old Fishery **A1–A14** (Gaedren + Gobblegut croc; orphans "Lamm's Lambs"); All the World's Meat **B1–B8** (Verik + Cow Hammer Boys + raktavarna spy); Eel's End **C1–C17** (Devargo "King of Spiders" + ettercap Chittersnap); Dead Warrens **D1–D13** (derro, undead, carrion golem, Vreeg CR6 boss).
- *Street Events 1–13* (riots, Grau Soldado CR5, otyugh, Queen audience, Guard briefings).
- *Subsystems:* First Harrowing; Korvosa Anarchy/Unrest city stats; Rumor Mill; **Shingles chase** (Trinia); knivesies; Devargo Diplomacy/bribe ladder; capture-alive (Verik); campaign-trait XP.
- *Key items:* Queen's Brooch, Zellara's haunted Harrow deck, Gaedren's coded ledger, raktavarna-dagger, Amprei letters, house drake Majenko.
- *Afflictions:* fool's leprosy (kills the king — plot), filth fever, shiver/dream-spider venom, blue whinnis, black adder venom.

**Ch2 — Seven Days to the Grave** (60/38/31/11/10/7)
- *Plague book.* Part 1 infection (smuggle Trinia, decoy ship *Direption*); Part 2 = **5 optional missions** (Direption wreck/Yvicca; wererat warren/Girrigz; Lavender fake-cure/Vendra; Racker's Alley vampire spawn; **Carowyn Manor**/Jolistina+21 zombies); Part 3 **Hospice of the Blessed Maiden** front over the hidden **Temple of Urgathoa (G)** — Dr. Davaulus (CR9), avoidable nosferatu **Ramoska Arkminos (CR14)**, **Lady Andaisin** (CR9 → daughter-of-Urgathoa CR8 two-phase).
- *Subsystems:* Second Harrowing; **Survivor Count** plague tracking (of ~5,000 doomed); Korvosa (Plagued) stats; **cure crafting**; hinterland/sewer encounter tables.
- *Afflictions (core):* **Blood Veil** (Con+Cha damage in PF1e), Vorel's phage, lycanthropy (wererats), ungol dust, energy drain (vampire spawn).
- *Hazard:* **Death's Breath Doors** (CR8 trap).

**Ch3 — Escape from Old Korvosa** (78/27/32/20/8/7)
- Quarantined island. Part 1 Red Mantis ambush at Vencarlo's (reveals Blackjack gear); meet **Laori Vaus**; artist Salvator Scream. Part 2 **Pilts Swastel** (CR10 bard "Emperor"), **Blood Pig** arena minigame. Part 3 **Arkona Palace** (rakshasas Bahor CR14 + Vimanda CR12) + sea-caves + the **Vivified Labyrinth** (rotating gear-dungeon, symbol traps, Sivit darksphinx, Senshiir asura) where Vencarlo + Neolandus are held.
- *Subsystems:* Third Harrowing; Old-Korvosa random encounters; quarantine travel; "Researching the Emperor" social ladder; **Blood Pig**; **Revolving Dungeon**; "Securing an Audience" social infiltration.
- *Notable risk:* Labyrinth lever-logic lets prepared parties **skip most of the dungeon** + missing maps for its 4 states (community-flagged); 6 symbol traps; coup-de-grace guillotine.

**Ch4 — A History of Ashes** (51/38/32/12/7/10)
- Cinderlands. Part 1 road north; 3 roving threats (Red Mantis **Cinnabar** CR12 + cleric **Koriantu** CR12; **Ashwing gargoyles**; **the Cinderlander** CR12). Part 2 **Respect-Point sandbox** (need 20): Acropolis of the Thrallkeepers (**havero** Noise-Point tentacles, multi-faction "Crowded Dungeon"), House of the Moon (**red reaver** CR13), Belly of the Beast (**Cindermaw** CR14 swallow-and-survive), **Trial of the Totem** (multi-day endurance + 6 bulettes), **Flameford Assault** (climax). Part 3 return to Korvosa: **Deathhead Vault** raid (Red Mantis + Gray Maiden leaders; rescue Marcus Endrin).
- *Subsystems (10):* Respect Points; Fourth Harrowing; **Havero Noise Points**; Game of Sredna; Trial of the Totem; Cinderlands travel; Cindermaw swallow/escape; Deathhead alarm escalation; city-stat shift (→Unrest); Blessing of the Ancestors ritual.

**Ch5 — Skeletons of Scarwall** (137/27/**68**/22/11/9) — the largest, most complex chapter
- Haunted Castle Scarwall (Kazavon's old seat). **Spirit-anchor subsystem:** Mithrodar (CR14 chained spirit) is unkillable until all **4 anchors** destroyed — **Belshallam** (umbral dragon CR14), **Castothrane** (skeleton warrior CR12; killable bloodlessly via his circlet), **Nihil** (ashmede devil CR13), **Zev Ravenka** (demilich CR14). Then Star Tower → Darklands → **Kleestad** (pharmakos CR15) guards **Serithtial** in the Sacred Lake.
- *Optional companions:* Laori + Sial as Ally/Enemy.
- *Subsystems (9):* Fifth Harrowing; the multi-layer **Scarwall Curse** (Dread/Aura of Menace/Soultrapping/Unhallow/Spiritual Doom); Brotherhood Ally/Enemy; Phantasms (scare set-pieces); **"A Swifter Scarwall"** official streamlining advice (p.330).
- *Risk:* huge crawl (~100+ keyed areas), undead attrition + energy drain everywhere, rest-cheese, many solo CR14–15 bosses, save-or-die wails. Community's #1 slog.

**Ch6 — Crown of Fangs** (118/27/28/8/5/7) — finale
- Part 1 **Rebellion-Point** streets (efreeti **Yzahnum**/Trifaccia; **Sabina + black dragon Zarmangarof** defection set-piece). Part 2 **Castle Korvosa** (~95 rooms — run as a **surgical strike, not a full clear**): erinyes, Gray Maidens, Red Mantis (**Kayltanya** CR15), **Togomor**/belier devil **Sermignatto** (CR16), **false-Ileosa blood simulacrum**, akaruzug, redeemable ghost **Venster** (→ Harrow Deck of Many Things). Part 3 **Sunken Queen** (Mushfens): boggard champions, devilfish Beirawash, scarlet walker Ithier CR17, 4 erinyes "furies", immortal ichor, then **Ileosa CR21** at the **Everdawn Pool** (6 simulacra + respawning blood-veil **taniniver** CR17). Conclusion: **"Rise of the Dragon"** — Kazavon CR25 rebuilds unless stopped (plunge **Serithtial** into the pool).
- *Subsystems:* Rebellion Points; Final Harrowing; Harrow Deck of Many Things; Mushfens travel; Ileosa's ritual timer (~10 days); castle patrol/alarm; city-stat tier.

**Appendices** (reference back-matter — convert as shared infrastructure)
- **App 2 Korvosa gazetteer:** 5 settlement stat blocks (baseline/Anarchy/Martial-Law/Plagued/Unrest), ~60 keyed city locations, district breakdown, **rumor subsystem**, hinterland stat blocks, regional environmental hazards.
- **App 3 The Harrow:** full harrowing subsystem, all **54 cards** (each keyed to an NPC/encounter), Harrow Points + per-chapter "Chosen" boon, Harrow Deck of Many Things.
- **App 4 Blood and Pain:** Blood Veil + kyton-eidolon subtype.
- **App 5 Equipment & Magic:** new poisons (fool's leprosy) + **artifacts** (Crown of Fangs, Everdawn Pool, **Serithtial**, Zellara's Harrow Deck).
- **App 6 NPC Codex:** master table + **12 full PF1e stat blocks** (CR 4–25) — the build targets for §3.1.
- **App 7 Bestiary:** 8 regional d% encounter tables + **9 new monsters** (CR ¼–24, incl. havero, chained spirit, pharmakos).

### 3.3 Subsystems → PF2e (master list)

| AP subsystem | Appears | PF2e target (Remaster) | Change-log |
|---|---|---|---|
| The Harrowing (54-card readings, Harrow Points, Chosen boon) | all ch + App 3 | Harrow Deck item + narrative reading; reroll pool → hero-point-style or *Harrowing* ritual | CHG-0010 |
| Harrow Deck of Many Things | Ch6 | Bespoke high-level magic item (translate 54 results) | CHG-0010 |
| Blood Veil plague + Survivor Count + daily exposure | Ch2 (App 4) | Virulent **disease** (Fort DC by level) + epidemic **clock/VP**; flat-check exposure | CHG-0011 |
| Korvosa settlement stat blocks (×5) + Rumor Mill | all + App 2 | Leveled item-availability table + city-state tiers driven by **Reputation**; rumor rolltables | CHG-0012 |
| Respect Points (Shoanti) / Rebellion Points / faction standing | Ch4, Ch6 | **Reputation** + **Victory Points** | CHG-0013 |
| Social/court influence (Devargo, doctors' soiree, Emperor research, war council) | Ch1–6 | **Influence** subsystem | CHG-0014 |
| Cinderlands overland travel | Ch4 | light **Hexploration** + Survival/Subsist | CHG-0015 |
| Shingles / fugitive **chases** | Ch1+ | **Chase** subsystem | CHG-0016 |
| Castle Korvosa / Hospice approach | Ch2, Ch6 | **Infiltration** subsystem | CHG-0017 |
| Minigames: knivesies, Blood Pig, Sredna, Trial of the Totem | Ch1,3,4 | Victory-Point skill challenges (PF2e action economy) | CHG-0018 |
| Scarwall spirit-anchor / chained-spirit / Curse | Ch5 | Bespoke ritual/condition + complex hazards; honor "Swifter Scarwall" | CHG-0019 |
| Havero Noise Points | Ch4 | Bespoke complex hazard / scaling reaction-creature | CHG-0020 |
| Campaign traits | Intro | PF2e **backgrounds** (custom "Korvosa hooks") | CHG-0021 |
| Korvosan Guard org-influence; Blackjack succession | App 6 | Reputation/Influence; archetype-style guidance | CHG-0022 |

---

## 4. Risk areas

### 4.1 Encounters likely overtuned/undertuned in PF2e
- **Solo bosses everywhere** (the dominant risk). PF1e single-creature fights collapse under PF2e's 4-action economy: Gaedren+Gobblegut (Ch1), Vreeg CR6 (Ch1 spike), Andaisin (Ch2), Pilts/Bahor/Vimanda (Ch3), Cindermaw/red reaver/catoblepas (Ch4), Mithrodar + 4 anchors + Kleestad (Ch5), **Ileosa CR21 + Kazavon CR25** (Ch6). → give lieutenants/minions/hazards/reactions or use PF2e Elite; **flag every PL+3/PL+4 solo** in the balance report.
- **Undertuned for endgame parties:** Gray Maiden street patrols (Ch6), Lamm himself (Ch1), the Ileosa finale as written. → troop/grouped stat blocks; harden the finale (phasing, reactive simulacra, throne-as-terrain).
- **Far-above-level spikes meant to be avoided:** Ramoska Arkminos CR14 (Ch2), Grau CR5 (Ch1), shared random-encounter tables spanning CR1→16 (App 7). → preserve the social/avoidance out; **party-level-gate** random tables.
- **Attrition chains:** Dead Warrens no-rest design (Ch1), Scarwall undead slog + rest-cheese (Ch5), Ch6 combat saturation (~12 wks). → rest points / anti-rest affliction / interleave Scarwall with Korvosa; trim filler.
- **Multi-faction / large-count fights:** Carowyn 21 zombies (Ch2), "A Crowded Dungeon" 3 factions (Ch4), 24 Ashwings/6 bulettes (Ch4), Everdawn 6 simulacra + furies + taniniver (Ch6). → stagger arrivals, troops, phasing.

### 4.2 PF1e mechanics that don't translate cleanly
- **Ability-score damage/drain** (Con+Cha for Blood Veil; Str/Dex/Wis/Int damage from poisons, Ithier's gaze, cytillesh, axiomatic whip) — PF2e has no ability damage → drained/enfeebled/clumsy/stupefied or HP.
- **Energy drain / negative levels** (vampires, wraiths, spectres, cinder ghouls, Serithtial, akaruzug) → drained/doomed/enervation.
- **Save-or-die / save-or-suck** (banshee/demilich wail, slay living, coup-de-grace guillotine, symbol traps, finger of death, irresistible dance, trap-the-soul) → PF2e degrees of success + **incapacitation trait**; rebuild as graded effects.
- **Alignment-keyed effects** (forbiddance, unhallow, holy/unholy weapons, rakshasa DR/good, "evil-only" wards) → PF2e holy/unholy traits + faction/passphrase exemptions (no alignment grid).
- **Class builds with no PF2e parity:** **vigilante** (Blackjack), **unchained summoner+eidolon** (Sial/Asyra), bloatmage (Togomor), cavalier (Kordaitra), skald, horizon walker, many multiclass NPCs → rebuild as bespoke PF2e NPCs at target creature level.
- **PF1e item/economy assumptions:** UMD + wand-charge economy, settlement Base Value/Purchase Limit, huge PF1e gp hoards (Kazavon's 100k+) → PF2e item access tables + Treasure-by-Level.
- **Disease/poison as fixed-DC Fort tracks**, "remove disease daily" cleric economy, permanency-based wards → PF2e affliction stages, Medicine/counteract math.
- **Haunts, simulacra, ghost rejuvenation, golem magic-immunity, rituals/artifacts** — all exist in PF2e but with different rules → per-element rebuild.

### 4.3 NPCs requiring full rebuilds (no clean official actor)
Most named villains/allies (App 6's 12 blocks + chapter bosses) are PF1e class-stacks → custom PF2e NPCs. Two-tier method (research §G.7): use an official **Monster Core/NPC Core/Bestiary** actor where a clean match exists (e.g., otyugh, ettercap→giant-spider-tier, gargoyle, bone/barbed/erinyes devils, mummy, banshee, purple worm for Cindermaw base, crocodile for Gobblegut); rebuild the rest. **No-parity specials:** Blackjack/vigilante, Sial+eidolon, havero, chained spirit, pharmakos, taniniver, akaruzug, scarlet walker, dybbuk/sayona/fext/penanggalen/manananggal (Tome-of-Horrors-style).

### 4.4 Story beats depending on PF1e-only assumptions
- **Campaign-trait revenge hook** (all PCs wronged by Lamm) → PF2e custom backgrounds; reinforce the "tie PCs to Korvosa, not just Lamm" QoL fix.
- **Fool's-leprosy kills the king** and resists cure → preserve narrative (no easy magical revive) without leaning on exact PF1e spell interactions.
- **"Only Serithtial harms Ileosa/Kazavon"** (regen bypass) → keep as story mechanic but ensure the party reliably has the sword; otherwise TPK risk.
- **Harrow as char-gen + recurring foreshadowing** → Harrow Deck item + per-chapter reading; reroll pool optional.
- **Plague resolves 1/3 in; back half leaves Korvosa** → adopt Anniversary-Edition Korvosa interludes + interleave Scarwall (QoL consensus).
- **Lore correction:** Kazavon is a **blue** dragon (not green); CR-25 form is a fail-state, not a standard fight.

### 4.5 Foundry import / structure risks
- **pf2e v7 actor/hazard schema** is the build target; custom NPCs must validate against it (run `validate.mjs` before each build). Schema drift on future system upgrades → re-extract/rebuild.
- **Stable `_id`s + UUID links** across journals↔actors↔hazards↔items↔scenes; broken links are the main import failure mode → covered by the validator.
- **No shipped maps/art** (copyright) → scene records reference **Racooze's battlemaps** by name; GM supplies legal copies. Vivified Labyrinth + the 4-state map gap is a known content hole to author as scene-planning notes.
- **Scope/size:** Scarwall (~137 areas) and Castle Korvosa (~95 rooms) are huge; default to the official **"Swifter Scarwall"** and **surgical-strike Castle** framings to keep the Foundry build (and play) tractable — documented as conversion changes.
- **Community stat-block links rot** (monster.pf2.tools / deprecated easytool.es) → we author our own actors rather than depend on external links.

---

## 5. Work plan

Phased per `PROJECT_PLAN.md`. Phase 1 (this audit + research + plan + change-log + scaffold) is **complete**. Next:

**Phase 2 — Pilot:** Chapter 1 opening — **the hunt for Gaedren Lamm → the Old Fishery (A1–A14)**, plus the immediate hooks it exercises (Zellara/First Harrowing, Lamm + Gobblegut boss, orphans as a non-combat moral element, fishery hazards, treasure incl. the Queen's Brooch + Harrow deck, capture/social DCs). This single slice validates: journal hierarchy & templates, PF2e actor JSON (Lamm custom + Gobblegut official-base), hazard JSON, encounter XP math, treasure-to-PF2e, DC conversion, the Harrow subsystem stub, and the change-log/validator loop — before scaling. Deliver the pilot's slice of every report.

**Phase 3 —** convert chapter-by-chapter (1→6 then appendices-as-infrastructure), building shared subsystems (Harrow, Blood Veil, Reputation/Influence, city tiers) early since they recur. Scarwall and the finale get extra balance scrutiny.

**Phases 4–5 —** cross-chapter consistency (recurring NPC builds, foreshadowing, level/treasure progression, faction continuity) then final QA → `FINAL_QA_REPORT.md`.

**Priority subsystem builds** (recur across many chapters, so do them in/just after the pilot): Harrow (CHG-0010), Korvosa city tiers + Reputation (CHG-0012/0013), campaign-trait backgrounds (CHG-0021). Blood Veil (CHG-0011) lands with Ch2.
