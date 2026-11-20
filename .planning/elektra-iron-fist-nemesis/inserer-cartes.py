"""Insere l'obligation et le set nemesis d'Elektra (63028-63033) et d'Iron Fist (64026-64029) dans data/cards.json.
Usage : .venv-linux/bin/python -I .planning/elektra-iron-fist-nemesis/inserer-cartes.py   (idempotent : refuse si 63029 existe)
Sources : vrais scans mc4db (.planning/elektra-iron-fist-scans-mc4db/) ; 63028 n'a qu'un apercu NON OFFICIEL
(play.marvelsimulator.com). Puis : tools/recalculer_checksums.py."""
import json
P = "Fusion/marvel-lcg-src/data/cards.json"
d = json.loads(open(P, encoding="utf-8").read())
EN, IN = "Elektra Nemesis", "Iron Fist Nemesis"
SHUF = "<b>When Defeated</b>: Shuffle this card into the encounter deck."

def carte(cid, typ, nom, desc, traits, set_name, text):
    return {"card_id": cid, "type": typ, "name": nom, "subtitle": "", "desc": desc, "traits": traits, "set_name": set_name, "text": text}

elektra = [
 # 63028 Conditioned by the Hand : RETIREE le 14/11/2026 (decision utilisateur) : pas de scan officiel, on attend.
 carte("63029", "Minion", "* Aka", {"HP": "4", "ATK": "2", "SCH": "2", "Nemesis": "Elektra", "Quickstrike": "1"}, ["HAND", "NINJA"], EN,
       "Quickstrike.\n" + SHUF + "\n<i>(Elektra's nemesis minion.)</i>\n<hr />\n[star] <b>Boost</b>: Deal Aka to the Elektra Natchios player as a facedown encounter card."),
 carte("63030", "SideScheme", "The Fist Fits in the Hand", {"Boost": "3", "Hazard": "1", "StartingThreat": "3"}, [], EN,
       "Each [[Hand]] minion gets +1 SCH and +1 ATK.\n<i>(Hazard Icon: Deal +1 encounter card during the villain phase.)</i>"),
 carte("63031", "Attachment", "Hand Katana", {"Boost": "2", "ATK+": "2"}, ["WEAPON"], EN,
       "Attach to the [[Hand]] minion with the highest base hit points. Otherwise, attach to the villain.\n<b>Hero Action</b>: Spend 2 resources of any type → discard this card."),
 carte("63032", "Minion", "Hand Blademaster", {"HP": "3", "ATK": "1*", "SCH": "1*", "Boost": "1"}, ["HAND", "NINJA"], EN,
       "[star] Hand Blademaster gets +1 SCH and +1 ATK if there is another [[Hand]] minion in play.\n" + SHUF),
 carte("63033", "Minion", "Hand Archer", {"HP": "3", "ATK": "1*", "SCH": "1", "Boost": "1", "Quickstrike": "1"}, ["HAND", "NINJA"], EN,
       "Quickstrike. <i>(After this minion engages your hero, it attacks you.)</i>\n[star] Hand Archer's attacks gain ranged.\n" + SHUF),
]
iron = [
 carte("64026", "Obligation", "Lack of Chi", {"Boost": "2", "GiveTo": "Danny Rand"}, [], IN,
       "<b><i>Give to the Danny Rand player.</i></b>\n<b>When Revealed</b>: Move all chi counters from your identity to this card.\n"
       "<b>Forced Interrupt</b>: When you would place a chi counter on Iron Fist, place it here instead. If there are at least 4 chi counters here, discard this card."),
 carte("64027", "Minion", "* Davos", {"HP": "5", "ATK": "2", "SCH": "1", "Boost": "2", "Nemesis": "Iron Fist"}, ["K'UN-LUN", "MARTIAL ARTIST"], IN,
       "<b>When Revealed</b>: Find and tuck the 3 Crane Daughter minions under here.\n<b>Forced Interrupt</b>: When Davos would take any amount of damage, "
       "shuffle a tucked Crane Daughter from under Davos into the encounter deck instead.\n<i>(Iron Fist's nemesis minion.)</i>"),
 carte("64028", "Minion", "Crane Daughter", {"HP": "3", "ATK": "2", "SCH": "2", "Boost": "2", "Vulnerable": "1"}, ["MYSTIC"], IN,
       "Vulnerable.\n<b>When Defeated</b>: Shuffle Crane Daughter into the encounter deck.\n<hr />\n[star] <b>Boost</b>: After this activation, tuck this card under Davos."),
 carte("64029", "SideScheme", "Steel Serpent", {"Boost": "2", "Acceleration": "1", "StartingThreat": "4"}, [], IN,
       "<b>Forced Interrupt</b>: When Davos attacks, discard a Crane Daughter tucked under him or defeat a Crane Daughter in play → Davos gets +3 ATK for this attack.\n"
       "<i>(Acceleration Icon: Place +1 threat on the main scheme at the start of the villain phase.)</i>"),
]
for pack, neuf, avant in (("elektra", elektra, "63034"), ("iron_fist", iron, "64030")):
    liste = d[pack]
    assert not any(c.get("card_id") == neuf[1]["card_id"] for c in liste), "deja insere"
    i = next(k for k, c in enumerate(liste) if c.get("card_id") == avant)
    liste[i:i] = neuf
    print(pack, len(neuf), "cartes inserees avant", avant)
open(P, "w", encoding="utf-8").write(json.dumps(d, indent=1, ensure_ascii=False) + "\n")
