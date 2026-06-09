# Treasure Report

Treasure is rebuilt to **PF2e Treasure-by-Level** (GM Core) — the community
conversion (Olliebird) deliberately omits treasure, so this is wholly ours
(CHG-0008). Story items keep their narrative weight but **not** their PF1e gp
(which would break PF2e's tight wealth math).

PF2e reference — **a full level 1** of treasure for a 4-PC party ≈ **175 gp total
value**, spread as: ~2 permanent items of level 1–2, a couple of consumables of
level 1–2, and ~40–60 gp currency. (Plus a slice of level-2's budget since the
fishery levels them to 2.)

> Scope: **Chapter 1 — Old Fishery (pilot)**.

## Converted parcels (Old Fishery)

| Source (area) | Original (PF1e) | Converted (PF2e) | Type | ~Value | Status |
|---|---|---|---|---|---|
| Gaedren (A13/14) | +1 dagger | **+1 dagger** (lvl 2 potency) | permanent | 35 gp | boss loot — first magic weapon |
| Gaedren (A14) | +1 padded armor | **+1 armor potency** (a worn leather/padded) *or* a level-2 minor item if no padded user | permanent | ~35 gp | boss loot |
| A14 hoard | wand of magic missile, ~2,375 gp gems/art | **Scroll of a 1st-rank spell** (e.g. *magic missile*/*grease*) + assorted gems re-priced to **~50 gp coin** | consumable + currency | ~60 gp | re-scaled hard down from PF1e |
| Yargin (A6) | wand of acid splash (28), acid ×3, thunderstone | **2× Acid Flask (lesser)** + **1× Thunderstone (lesser)** | consumables | ~8 gp | cantrip-wand → flasks |
| Yargin (A6) | garnet amulet 100 gp | **Garnet** gem | currency | 8 gp | `garnet-amulet.json` |
| A13 table | darkwood coffer + 20 shiver + 7 vermin repellent | **Coffer (~10 gp) + 7 vermin repellent** (shiver = story, not loot) | item + tool | ~12 gp | `coffer-of-shiver.json`; repellent trivializes the spider nest |
| Thug gear (A5–A8) | misc weapons/armor, ~150 gp coin, 3 CLW potions | **~30 gp coin** + **3× Healing Potion (minor)** | currency + consumable | ~30 gp + potions | Giggles' potions |
| A14 ledger | (worth 250/500 gp Guard bounty) | **Guard bounty 15 gp (30 gp w/ cipher key)** | quest currency | 15–30 gp | `gaedrens-coded-ledger.json` |
| **Queen's Brooch** (A14) | 2,000 gp art; 1,200 gp reward | **Story item (loot value ~25 gp)**; **queen's reward = a level-1 parcel** (≈ 40 gp + a level-2 consumable) at Event 8, *next chapter section* | story → reward | reward booked to Event 8 | `queen-ileosas-brooch.json` |
| **Zellara's Harrow Deck** (A14) | intelligent item (priceless) | **Story item** (Harrow subsystem anchor) — no gp | story | — | `zellaras-harrow-deck.json` |

### Totals & budget check (pilot)
- **Permanent items:** +1 dagger, +1 armor potency (2 level-2 permanents) — ✅ matches the "~2 permanents" expectation for level 1→2.
- **Consumables:** scroll (1st), 2 acid flasks, thunderstone, 3 minor healing potions — ✅ healthy consumable spread for a first dungeon.
- **Currency (in-fishery):** ~50 (hoard) + 8 (garnet) + 12 (coffer) + 30 (thug coin) ≈ **~100 gp**, + ledger bounty 15–30 gp = **~115–130 gp**.
- **Verdict:** **slightly under** a full level-1 + partial level-2 budget *inside the fishery* — **by design**, because the **queen's reward (Event 8) tops it off** with the next parcel. Net for the chapter opening lands on-budget. ⚠️ Do **not** restore PF1e gp values (would overshoot by ~10×).

### Story-critical item tracking
- **Queen's Brooch** → launches Event 8 (queen audience) → recruitment + reward.
- **Zellara's Harrow Deck** → the recurring Harrow subsystem (CHG-0010); becomes the Harrow Deck of Many Things in Ch.6.
- **Coded ledger** → 'Framed' background payoff + Guard bounty.
- **Vermin repellent** → soft key that trivializes the A11 spider nest (reward for looting A13 first).

### Consumable vs permanent vs currency distribution (pilot)
- Permanent: 2 · Consumable: ~6 · Currency: ~115–130 gp + reward parcel. Balanced for a level 1→2 opener.

*(Later chapters append per-chapter treasure tables here.)*
