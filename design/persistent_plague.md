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

## Approval
☐ **Approve** → I implement this in the Ch.2 conversion and thread the status beats
through Ch.3–6, with Major change-log entries.
☐ **Adjust** → tell me what to change (e.g. exposure weight, clock pacing).
☐ **Revert to faithful** → plague resolves in Ch.2.
