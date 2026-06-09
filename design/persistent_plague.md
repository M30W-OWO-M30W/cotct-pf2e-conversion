# Design Proposal — Persistent Blood Veil Plague

> **STATUS: `REQUIRES GM APPROVAL` (Major story change).** Not implemented in any
> playable journal until approved. Tracked as **CHG-0011 (revised → Major)** in
> `conversion_change_log.md`.

GM decision (2026-06-09): run Blood Veil as a **persistent background threat**
across the whole AP rather than an arc resolved in Chapter 2. This documents how it
works and its story impact, for sign-off.

## The core idea (and why it's lore-coherent, not just a houserule)

In the AP as written, the PCs craft a cure at the end of Ch.2 and the plague burns
out — retiring the campaign's creepiest beat one-third in. The persistent version
keeps the dread alive **and ties it to canon**: Ileosa doesn't just want power, she
wants Korvosa's **blood and death** to fuel her immortality. Two things the AP
already establishes make the plague a *deliberate, ongoing* harvest rather than a
random outbreak:

- **"The Blooding"** (Appendix 1 background event) — an Asmodean temple secretly
  collects citizens' blood for Ileosa.
- **The Everdawn Pool** (Ch.6 finale artifact) — a blood-powered immortality engine
  that consumes the dying.

So: **Blood Veil is the front end of Ileosa's blood harvest.** The Ch.2 "cure"
*suppresses* the acute outbreak (saving the city from immediate collapse — the
Survivor Count still matters), but the Urgathoa/Red Mantis machinery keeps
**re-seeding** it at a slow burn, because a steadily dying city feeds the Pool. It
only truly ends when **Ileosa falls** (Ch.6). This *strengthens* the throughline
and pays off the Ch.2 beat at the finale.

## How it works mechanically (PF2e)

A single lightweight overlay — an **Epidemic Clock** — on top of the already-planned
PF2e disease (Player Core) + city-tier (Reputation) systems. No new dice subsystem.

1. **Epidemic Clock (0–10).** Represents the plague's grip on Korvosa.
   - Ch.2 end: the suppressant cure drops it from "outbreak" to a low simmer
     (set by the Survivor Count — more saved = lower start).
   - **Advances** +1 per in-city downtime week, and faster (+1 extra) **while the
     PCs are away** (Ch.4 Cinderlands, Ch.5 Scarwall) — they return to a sicker
     city. Re-seeding events (a new tainted-coin batch, a cult cell) bump it.
   - **Recedes** −1 when PCs spend a downtime action or complete a beat against it
     (distribute cure, burn a cult cell, expose a Blooding site).
2. **Drives the Korvosa city tier.** Clock ≥7 → the **Plagued** city stat block
   stays/returns (worse item availability, grimmer NPC attitudes, Reputation
   pressure); ≤3 → recovers toward Unrest/Martial Law per the political plot.
3. **Per-PC exposure** continues only at a **low** level in the city (a flat-check
   far gentler than the Ch.2 acute outbreak — atmosphere, not attrition). Uses the
   same PF2e Blood Veil disease block (CHG-0011 base).
4. **The finale closes it.** Defeating Ileosa / destroying the Everdawn Pool ends
   the re-seeding; the clock empties over the denouement. (If the PCs *fail* — the
   "What If Ileosa Wins" scenario — it maxes out.)

## Chapter-by-chapter story impact

| Chapter | What changes vs. faithful | Effort |
|---|---|---|
| **Ch.2** | The crafted cure is a **suppressant**, not eradication. Andaisin/the Hospice fall, but the cult's re-seeding survives. Survivor Count sets the clock's start. Add 1–2 lines of foreshadowing that "this isn't over." | Low (reframe the conclusion) |
| **Ch.3** | Old Korvosa is plague-scarred (already true). The clock simmers; occasional flare-ups. Rook the plague-doctor / survivors gain weight. **No structural change.** | Very low |
| **Ch.4** | PCs leave for the Cinderlands → **clock advances unchecked**; they return (Deathhead raid) to a visibly worse city. Raises the stakes of leaving. | Low (a status beat at depart/return) |
| **Ch.5** | PCs leave for Scarwall → clock advances again. **Reinforces the #1 QoL fix** (interleave Scarwall with Korvosa) — they feel the city dying while dungeon-crawling. | Low |
| **Ch.6** | The plague is revealed as part of Ileosa's blood harvest (Blooding + Everdawn Pool); ending her ends it. **Payoff for the Ch.2 beat.** | Low (tie-in text; the finale already exists) |

## What's preserved vs. changed

- **Preserved:** all locations, encounters, villains, the Ch.2 dungeon, the Survivor
  Count, the political plot, and the existing finale. The plague overlay rides *on
  top of* the as-written structure — it doesn't delete or relocate content.
- **Changed (the Major part):** the Ch.2 cure becomes suppressant-not-cure, and a
  light plague-status beat is threaded into Ch.3–6. This is a genuine deviation from
  "the plague is solved in Ch.2," hence the approval gate.
- **Net effort:** moderate and front-loaded into the Ch.2 conversion + a recurring
  one-paragraph "Plague Status" block per later chapter. Much cheaper than the full
  sandbox "rebellion-rating" rewrite (which we are **not** doing).

## Risks / things to confirm
- **Tone:** a never-ending plague can feel grindy. Mitigation: keep per-PC exposure
  *light* (atmosphere) and make the clock respond to player action so it feels
  agentive, not punishing.
- **Continuity bookkeeping:** the clock + city tier must be tracked across chapters
  (a campaign-state journal page will hold it).
- **Decoupling option:** if it drags at the table, the GM can declare the cure
  eradicates it (revert to faithful) at any chapter break with zero downstream
  breakage — the overlay is designed to be removable.

## Consequences & GM options (what "too far" costs) — APPROVED ADDENDUM

The clock must **bite**, with the GM steering *how*. Consequences escalate by tier
and recede when the PCs act. The only **permanent** cure is Ileosa's defeat (Ch.6);
everything before is suppression.

### Escalation by Epidemic Clock tier

| Clock | State | City tier | What the table feels (GM picks from the menus below) |
|---|---|---|---|
| **0–3** | Receding / contained | Unrest→recovering | Flavor only; markets recover; grateful NPCs. The PCs' wins are visible. |
| **4–6** | Simmering | Plagued looms | Quarantine checkpoints; some goods scarce; a *minor* Reputation/attitude drag; **one personal hook** fires (an NPC the PCs know falls ill). |
| **7–8** | Spreading | **Plagued active** | Harsher item availability & prices; worse NPC attitudes; a district goes under quarantine; **lose an NPC or a place**; the Korvosan Guard's support capacity drops (soft penalty to later aid). |
| **9** | Crisis | Plagued + Martial Law | Riots/brutal crackdowns; a district effectively lost; allies pressure the PCs to drop side-goals; a safe haven becomes unusable. |
| **10** | Catastrophe ("too far") | Anarchy / collapse | **Point-of-no-return:** Ileosa's harvest accelerates — the **Everdawn Pool gains charges early, shortening the Ch.6 ritual timer** — *and/or* a mass-death event permanently darkens the denouement. Not a TPK; the **world** pays. |

### GM options menu (pick what hurts *this* table)
- **A · PC infection.** If a PC fails enough exposure flat-checks, they contract
  Blood Veil (the CHG-0011 staged disease: Fort save, drained/enfeebled by stage).
  Three tones the GM can choose: **Gritty** (real risk, must self-treat with
  Medicine/magic or worsen), **Heroic** (curable with effort — a fetch for the
  suppressant), or **Grim** (a PC carries a managed strain as a recurring
  complication and personal stake). Always give an *out*, never a death spiral.
- **B · Lose an NPC.** A tiered "who the plague can take" list — throwaway contact
  (tier 4–6) → named ally/quest-giver (tier 7–9). GM picks by emotional weight; this
  is the primary stakes lever and the payoff for "the city is dying around you."
- **C · Lose a place.** A safe house, a favored shop, or a whole district becomes
  quarantined/unusable — concrete, reversible-by-action loss.
- **D · Faction cost.** Korvosan Guard / church of Abadar support weakens (ties to
  the Reputation system), making later-chapter aid thinner — a *soft mechanical*
  consequence the players can see coming and prevent.
- **E · Accelerate the villain.** High clock feeds the Everdawn Pool → the Ch.6
  ritual timer is shorter, the finale tenser. (The mechanical bridge from Ch.2's
  neglect to Ch.6's stakes.)
- **F · Moral pressure.** NPCs beg the PCs to prioritize the plague over the
  political plot; either choice has consequences (no wrong answer, real tension).

### Player agency (so it feels earned, not punitive)
- **Ignoring it** → clock climbs faster (+1 extra per in-city week; the away-chapter
  bumps stack). **Fighting it** (downtime actions: distribute the suppressant, burn a
  cult cell, expose a Blooding site, fund the church) → −1 each and can hold tiers.
- Every consequence above is **telegraphed one tier early** (NPCs warn, news
  spreads) so players can choose to spend resources averting it.
- **Removable:** at any chapter break the GM may rule the suppressant became a true
  cure (revert to faithful) with zero downstream breakage.

## Approval
☑ **APPROVED as specified (2026-06-09)**, with this consequences/GM-options addendum.
Implement in the Ch.2 conversion + thread light "plague status" + the clock/
consequences menu through Ch.3–6, with Major change-log entries and a campaign-state
journal page to track the clock. Keep per-PC exposure light and consequences
telegraphed; preserve the removability hatch.
