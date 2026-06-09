# DC & Skill Conversion Report

PF1e DCs are **not** transliterated. PF2e DCs use the **level-based DC table**
(GM Core) and **simple DCs** (Untrained 10 / Trained 15 / Expert 20 / Master 30 /
Legendary 40), adjusted ±2/±5 for hard/incredibly-hard tasks. Level-based DC
anchors used here: **L0 = 14, L1 = 15, L2 = 16, L3 = 18**.

Skill renames applied: Disable Device → **Thievery**; Sense Motive → **Perception**;
Linguistics(decode) → **Society** (or relevant Lore); Escape Artist → **Athletics
(Escape)/Acrobatics (Squeeze)**; UMD → folded into items.

> Scope: **Chapter 1 — Old Fishery (pilot)**.

| Check (area) | PF1e | PF2e | DC basis | Success / Failure |
|---|---|---|---|---|
| See through Zellara's illusion (Zellara's Home) | Will DC 25 | **Will DC 18** | Lvl-based (hard, L1) | Succeed: perceive the room/Zellara as ghostly/ephemeral (she's still benign). Fail: it reads as real. Not required to proceed. |
| Pick the locked doors A1/A3/A7-cabinet/A13 | Disable Device DC 20 | **Thievery DC 15** (A13's tiny door DC 17) | Simple (Trained); +2 for the awkward 2½-ft A13 door | Succeed: open. Crit fail: jam (must Force Open, Athletics DC 17). Brass key (Yargin/Gaedren) bypasses all. |
| Spot the hidden trapdoor (A6) | Perception DC 25 | **Perception DC 18** (Seek) | Lvl-based (hard, L1) | Succeed: find the barred trapdoor to A13. Fail: missed (it's a shortcut/flank, not required). |
| Force the barred trapdoor (A6) | break DC 15 | **Athletics DC 17** (Force Open) | Simple (Trained, +2) | Succeed: smash through to A13 (a flanking route onto the boss). |
| Squeeze through the 1-ft trap-hole / pilings | Escape Artist DC 30 | **Acrobatics DC 20 (Squeeze)**, Small only | Simple (Expert) | Tiny/Small creatures only; mostly flavor. |
| Cross the Slippery Boardwalk (A3) | Acrobatics DC 10 (move >speed) | **Reflex/Acrobatics DC 15** (on the hazard) | Lvl-based (L1) | Fail: prone. Crit fail: fall 13 ft into shark water (A12). Step (5 ft) = safe. *(Hazard `slippery-boardwalk`.)* |
| Rotten foredeck (A9) | Reflex DC 12 | **Reflex DC 16** | Lvl-based (L1, hard) | Fail: crash to A11 for 1d6 + prone among the spiders. Stern is safe. *(Hazard `rotten-ship-deck`.)* |
| Climb the river embankment | Climb DC 10 | **Athletics DC 15** (Climb) | Simple (Trained) | Slippery 13-ft bank up from the river. |
| Spot Gaedren's secret door (A11) | Perception DC 20 (+10 w/ Survival DC 15 tracks) | **Perception DC 17** (Seek); a successful **Survival DC 15** to Track first gives **+2 circumstance** | Lvl-based + aid | Finds the hull door to A12/A13. |
| Rally an orphan to your side | Diplomacy DC 15 (Intimidate fails) | **Diplomacy DC 15** (Intimidation auto-fails — kids are inured) | Simple (Trained) | Succeed: orphan can Aid or reveal info. Fail (no retry while threatened): the orphan cowers; if a thug looms, may be forced to act for them. |
| Spot Hookshanks among the orphans (A7) | (opposed Disguise) | **Perception DC 17** vs his Deception | Lvl-based (hard) | Succeed: notice the gnome imposter before he Sneak Attacks. |
| Decode Gaedren's ledger (A14) | Linguistics DC 15 (Varisian) | **Society DC 17** (must read Varisian), a few hours | Lvl-based (hard, L1) | Succeed: bounty 15 gp (30 gp w/ cipher key); 'Framed' payoff. |
| Note Zellara's head is weeks-dead (A14) | Heal DC 10 | **Medicine DC 14** | Lvl-based (L0) | Succeed: realize the fortune-teller has been dead for weeks (the reveal). |
| Talk down / read Gaedren | (varies) | **Perception** (his Deception +10) for lies; **Diplomacy DC 20** to parley | Lvl-based (hard) | Mostly flavor — he's the kill/capture target, not a social out. |

## Notes
- **Locked-door spam** (PF1e DD 20 everywhere) collapses to a couple of **Thievery DC 15** picks; the brass key removes most of it — keep the *flow*, not the dice-rolling.
- **Hazard saves** (boardwalk/deck) are encoded in the hazard actors' reactions with inline `@Check[...]`/`@Damage[...]` so they auto-roll in Foundry.
- **No PF1e ability/skill that lacks a PF2e analog** appears in the pilot; the only judgment calls are the "hard-task +2/+5" adjustments, all noted above.

*(Later chapters append their DC tables here.)*
