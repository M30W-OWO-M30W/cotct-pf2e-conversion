#!/usr/bin/env python3
"""Appendices & Beyond — the post-finale arc (CHG-0003), campaign artifacts,
gazetteer references, and the cross-chapter dramatis personae index."""
from __future__ import annotations
import copy
import pf2e_build as B

MODID = "cotct-pf2e-conversion"
ITEM_ROOT, ADV_FOLDER = "cotctItemRoot001", "cotctAdvFolder01"

JIDA = "appendicesBeyond"
ARTIFACT_FOLDER = "campaignArtifct1"
SERITHTIAL_ID, CROWN_ID = "serithtialSword1", "crownOfFangs0001"

ids = B._idgen(770007)
def nid(): return next(ids)
sids = B._idgen(887007)
def sid(): return next(sids)

def act(_id, label): return f"@UUID[Compendium.{MODID}.cotct-actors.Actor.{_id}]{{{label}}}"
def itm(_id, label): return f"@UUID[Compendium.{MODID}.cotct-items.Item.{_id}]{{{label}}}"
def chk(s): return f"@Check[{s}]"
def SEC(html): return B.s_secret(html, sid())

B.write("items", "_folder_campaign-artifacts-ite",
        copy.deepcopy(B.folder(ARTIFACT_FOLDER, "Campaign Artifacts", "Item", ITEM_ROOT, 300000, "#b3541e", "a")))

# ---- the two great artifacts as real items ----
B.write("items", "serithtial", B.equipment(SERITHTIAL_ID, "Serithtial", 20, 0,
  "<p><strong>Artifact — the bane of Kazavon.</strong> The bastard sword of Mandraivus, forged by the Esoteric Order of the Palatine Eye and quenched in the dragon's own defeat. Recovered from the Sacred Lake beneath Scarwall (Ch.5, H4), <strong>suppressed</strong> (a masterwork blade) until the Scarwall curse breaks — then fully woken.</p>"
  + "<p><strong>Awakened:</strong> a <em>+3 major striking keen holy bastard sword</em> (treat as a d12 two-hand sword with deadly d10). Against creatures bearing any fragment of Kazavon's essence (the Crown's wearer, the taniniver, Kazavon himself): +4 status damage per die. <strong>Suppresses Queen Ileosa's regeneration</strong> while it has damaged her this round; each hit forces her "+chk("type:fortitude|dc:35")+" or "+B.cond("drained", "Drained 1")+" (cumulative). <strong>Only Serithtial can sunder the Crown of Fangs</strong> (Hardness 20, HP 80 against this blade alone).</p>"
  + "<p><strong>Intelligent &amp; choosy:</strong> Serithtial favors a good-hearted bearer (she <em>chooses</em>; an unworthy hand finds her merely sharp). She speaks rarely, remembers Mandraivus, and wants one thing: the seed of Kazavon dead forever. Near-indestructible (artifact).</p>",
  traits=["artifact", "magical", "holy", "unique"], rarity="unique", folder=ARTIFACT_FOLDER))

B.write("items", "crown-of-fangs", B.equipment(CROWN_ID, "The Crown of Fangs", 22, 0,
  "<p><strong>Artifact — Midnight's Teeth.</strong> Queen Ileosa's crown, self-forged around the fangs of Kazavon; the vessel of the dragon's soul-seed. While worn: <strong>regeneration 20</strong> (suppressed only by <em>Serithtial</em>), <em>mirror image</em> at will, <em>dominate</em> 3/day ("+chk("type:will|dc:42")+"), continuous true seeing — and the wearer cannot truly die. The second soul grows with every day worn and every death defied; a non-Ileosa wearer begins the campaign's horror over again ("+chk("type:will|dc:40")+" per week or the whispers take root).</p>"
  + "<p><strong>Destruction:</strong> only <em>Serithtial</em> can sunder it (Hardness 20, HP 80 vs. that blade; effectively indestructible otherwise). Its destruction kills the soul-seed — screaming — and ends the regeneration instantly. The six other relics of Kazavon (Armor of Skulls, Bound Blade, Howling Horn, Shredskin, Staff of the Slain, Throne of Nalt) remain scattered across Avistan…</p>",
  traits=["artifact", "magical", "unholy", "unique"], rarity="unique", folder=ARTIFACT_FOLDER))

# ---- journal ----
pages = []
def PG(name, html, level=2): pages.append(B.page(nid(), name, html, level=level))

PG("Continuing the Campaign — the Post-Finale Arc",
  B.s_milestone("<p><strong>Beyond the Crown (L17–20, optional).</strong> The approved postgame (CHG-0003): the main story closes at L17; these seven seeds — three of them developed into a playable arc — carry the table to 20 in the same world they saved.</p>")
  + "<p><strong>ARC I — Rulers of Korvosa (L17, intrigue):</strong> no monarch in a century of curses. Neolandus runs the restoration and asks the PCs to broker the succession; factions (the noble houses, the church of Abadar's schism, the surviving Arkonas' papers, the freed Gray Maidens) maneuver. Run it as Influence — and let a PC end it on the Crimson Throne, with everything that word now means.</p>"
  + "<p><strong>ARC II — Sorshen's Legacy &amp; the Everdawn Pool (L18, dungeon):</strong> the Pool's residue stirs what sleeps beneath the city — the pyramid under Castle Korvosa was <em>hers</em>. Destroying the artifact for good is a high-level expedition into Thassilonian deeps; using it, even once, invites Eurythnia's leftovers up the crystal veins.</p>"
  + "<p><strong>ARC III — Kazavon Rises (L19–20, the true endgame):</strong> the Crown was one relic of seven. Across Avistan the others — Armor of Skulls, Bound Blade, Howling Horn, Shredskin, Staff of the Slain, Throne of Nalt — begin to <em>converge</em>, carried by owners who dream the same dream. If they meet, the dragon is reborn whole. Serithtial knows it; she has been waiting five hundred years to finish this. The finale the campaign earns: Kazavon, complete, and one sword.</p>"
  + SEC("<p><strong>Side-seeds</strong> (thread into the arcs): <strong>Ileosa's Revenge</strong> — her soul went to Hell under contract; she can bargain her way back (a devil-army vengeance, or a vampire-return via Pool blood-magic). <strong>Lorthact's Plot</strong> — the contract's hidden master is the exiled Infernal Duke ruling the Acadamae in secret; Ileosa's soul may be his ticket home, and his enemies pay well. <strong>A New Crimson Peril</strong> — the Red Mantis remember: the Crimson Citadel raid is 'harder than Scarwall' (and if Cinnabar lives redeemed, they remember her most of all).</p>"))

PG("Campaign Artifacts",
  "<p>The campaign's three great objects, as items: "+itm(SERITHTIAL_ID, "Serithtial")+" · "+itm(CROWN_ID, "The Crown of Fangs")+" · and <strong>Zellara's Harrow Deck</strong> (Ch.1 items folder), which in the endgame may transcend into the <strong>Harrow Deck of Many Things</strong> (CHG-0010): each of the 54 cards a fate, drawn at the GM's table-knowing discretion — the suit boons of the Harrowing, made permanent and dangerous.</p>"
  + SEC("<p><strong>The Everdawn Pool</strong> (not lootable, mercifully): a major artifact of stored life — each charge a day of stolen blood. Its post-campaign residue is Arc II's hook; its destruction is Arc II's prize.</p>"))

PG("Korvosa & Beyond (Gazetteer Reference)",
  "<p><strong>The city</strong> (Appendix 2's 84 keyed locations, summarized for play): the Heights (Castle Korvosa, the Acadamae — Lorthact's secret), Old Korvosa (Endrin Isle, Old Dock, Fort Korvosa — the Arkonas), North Point (the Bank of Abadar, Citadel Volshyenek, the Longacre Building), Midland (the Shingles, Eel's End), Gray District (the Dead Warrens, the rebel ossuary), South Shore (Carowyn Manor, the noble estates), East Shore (Hellknight Citadel Vraid beyond).</p>"
  + "<p><strong>City state-tracking:</strong> run Korvosa's condition by the Conversion Guide's <strong>Reputation &amp; City Tiers</strong> page (Anarchy → Martial Law → Plagued → Unrest → recovering), driven by the <strong>Epidemic Clock</strong> (Blood Veil page) and the chapters' events. <strong>The Rumor Mill:</strong> a gather-information beat per downtime ("+chk("type:diplomacy|dc:15")+" to "+chk("type:diplomacy|dc:25")+" by tier) keeps the city talking.</p>"
  + "<p><strong>The hinterlands:</strong> Harse (Blackbird Ranch, Trots), Kaer Maga (the cliff-city resupply), the Cinderlands (Appendix-2 environment rules: heat, ash storms, thirst — used in Ch.4), the Mushfens (Ch.6's swamp road), Belkzen and the World's Edge passes (Ch.5's road).</p>")

PG("Dramatis Personae (Campaign Index)",
  '<p class="subhead"><strong>Allies & Patrons</strong></p>'
  + "<ul>"
    "<li><strong>Cressida Kroft</strong> — Field Marshal; patron from Ch.1, rebel leader by Ch.6</li>"
    "<li>"+act("vencarloOrisini1", "Vencarlo Orisini")+" — swordmaster, mentor — and Blackjack (Ch.3+)</li>"
    "<li>"+act("neolandusKalep01", "Neolandus Kalepopolis")+" — the missing seneschal; the lawful lever (Ch.3+)</li>"
    "<li>"+act("triniaSabor00001", "Trinia Sabor")+" — the framed painter (Ch.1-2, returns Ch.4)</li>"
    "<li>"+act("grauSoldado00001", "Grau Soldado")+" — redeemed watch sergeant (Ch.1-2)</li>"
    "<li>"+act("ishaniDhatri0001", "Ishani Dhatri")+" — Abadaran healer of the plague (Ch.2+)</li>"
    "<li>"+act("aminJalento00001", "Amin Jalento")+" — rescued young noble (Ch.1, 3, 6)</li>"
    "<li><strong>Thousand Bones</strong> — Skoan-Quah shaman; the Shoanti door (Ch.1, 4)</li>"
    "<li>"+act("krojunEatsWhat01", "Krojun Eats-What-He-Kills")+" — Sklar-Quah champion; rival, then nalharest (Ch.4)</li>"
    "<li>"+act("akramTruthspeak1", "Truthspeaker Akram")+" — the last truthspeaker (Ch.4)</li>"
    "<li>"+act("marcusEndrin0001", "Marcus Endrin")+" — Sable commandant; the great rescue (Ch.3, 4)</li>"
    "<li>"+act("laoriVaus0000001", "Laori Vaus")+" — cheerful Kuthite; the long redemption (Ch.3, 5)</li>"
    "<li>"+act("shadowcountSial1", "Shadowcount Sial")+" — Brotherhood of Bones; would-be curate (Ch.4-5)</li>"
    "<li>"+act("sabinaMerrin0001", "Sabina Merrin")+" — the queen's general; the great defection (Ch.6)</li>"
    "<li>"+act("vensterArabast01", "Venster's ghost")+" — the kindest informant (Ch.6)</li>"
    "<li><strong>Zellara</strong> — the harrow-spirit guide (whole campaign; guard her from Scarwall)</li>"
   "</ul>"
  + '<p class="subhead"><strong>Villains, by Chapter</strong></p>'
  + "<ul>"
    "<li><strong>Ch.1</strong> — "+act("RKfT6vJ5guinSBjo", "Gaedren Lamm")+" · "+act("vreegDerroNec001", "Vreeg")+"</li>"
    "<li><strong>Ch.2</strong> — "+act("reinerDavaulus01", "Dr. Davaulus")+" · "+act("andaisinUrgath01", "Lady Andaisin")+" · "+act("ramoskaArkminos1", "Ramoska Arkminos")+" · "+act("jolistinaSusp001", "Jolistina")+"</li>"
    "<li><strong>Ch.3</strong> — "+act("piltsSwastel0001", "Pilts Swastel")+" · "+act("bahorArkona00001", "Bahor")+" · "+act("vimandaArkona001", "Vimanda")+" · "+act("sivitDarksphinx1", "Sivit")+"</li>"
    "<li><strong>Ch.4</strong> — "+act("cinderlander0001", "the Cinderlander")+" · "+act("cinnabarRedMant1", "Cinnabar")+" · "+act("zenobiaZenderh01", "Zenobia Zenderholm")+" · "+act("kordaitraDesta01", "Kordaitra Destaid")+"</li>"
    "<li><strong>Ch.5</strong> — "+act("mithrodarChain01", "Mithrodar")+" · "+act("zevRavenkaDemi01", "Zev Ravenka")+" · "+act("belshallamUmbr01", "Belshallam")+" · "+act("kleestadPharma01", "Kleestad")+"</li>"
    "<li><strong>Ch.6</strong> — "+act("togomorBloatmg01", "Togomor")+" · "+act("sermignattoDvl01", "Sermignatto")+" · "+act("kayltanyaRedM001", "Mistress Kayltanya")+" · "+act("queenIleosa00001", "QUEEN ILEOSA")+"</li>"
   "</ul>"
  + B.s_conv("<p><strong>Module complete:</strong> Chapters 1–6, four subsystems (Harrowing · Reputation/City Tiers · Blood Veil/Epidemic Clock · Respect &amp; Rebellion Points), the campaign backgrounds, and the postgame arc. Verbatim read-aloud renders only on the GM's machine (local AP.md injection); all mechanics are original PF2e conversion work. Run well.</p>"))

journal = B.journal_entry(JIDA, "7. Appendices & Beyond", pages, folder=ADV_FOLDER)
B.write("journals", "07-appendices-and-beyond", copy.deepcopy(journal), embed_pages=True)
print(f"Appendices built: 2 artifacts, 1 journal ({len(pages)} pages).")
