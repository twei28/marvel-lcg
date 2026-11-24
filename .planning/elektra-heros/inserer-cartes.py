"""Insere les cartes du HEROS Elektra (63001a a 63014) dans data/cards.json, pack `elektra`, avant 63015.
Usage : .venv-linux/bin/python -I .planning/elektra-heros/inserer-cartes.py   (idempotent : refuse si 63001a existe deja)
Texte contre scan : voir .planning/elektra-heros/PLAN.md. Puis : tools/recalculer_checksums.py."""
import json
P = "Fusion/marvel-lcg-src/data/cards.json"
raw = open(P, encoding="utf-8").read()
d = json.loads(raw)
liste = d["elektra"]
assert not any(c.get("card_id") == "63001a" for c in liste), "deja insere"
H = "Elektra"
NIN = "Elektra Ninja"
NINJA_BOOST_SI = "[star] <b>Boost</b>: If Elektra is using a basic power, "

def carte(cid, typ, nom, desc, traits, set_name, text, sub=""):
    return {"card_id": cid, "type": typ, "name": nom, "subtitle": sub, "desc": desc,
            "traits": traits, "set_name": set_name, "text": text}

def ninja(cid, nom, effet):
    return carte(cid, "Treachery", nom, {"Surge": "1"}, ["NINJA"], NIN,
        "Surge. <i>(After this card is revealed, reveal 1 additional encounter card.)</i>\n"
        "<b>When Revealed</b>: Give this card to Elektra as a facedown boost card.\n<hr />\n"
        + NINJA_BOOST_SI + effet + " Otherwise, give this card to Elektra as a facedown boost card.")

neuf = [
 carte("63001a", "Hero", "* Elektra",
       {"HP": "9", "ATK": "1", "THW": "0", "DEF": "1", "HS": "5", "Villainous": "1"},
       ["DEFENDER", "MARTIAL ARTIST"], H,
       "[star] Villainous. <i>(When this character uses a basic power, give it a boost card.)</i>\n"
       "<i>Killer Instinct</i> — <b>Interrupt</b>: When a boost card given to Elektra is turned faceup, cancel its \"Boost\" ability. Then, that card gains [boost]."),
 carte("63001b", "AlterEgo", "* Elektra Natchios", {"HP": "9", "REC": "3", "HS": "6"}, ["ASSASSIN"], H,
       "Elektra Natchios begins the game with a [[Ninja]] deck. <i>(See insert.)</i>\n"
       "<i>Ninja Training</i> — <b>Interrupt</b>: When you change to hero form, shuffle the top card of the [[Ninja]] deck into the encounter deck."),
 ninja("63002", "Ninja Stars", "draw 2 cards and shuffle this card into the [[Ninja]] deck."),
 ninja("63003", "Ninja Strike", "she gets +3 to that power for this use and you shuffle this card into the [[Ninja]] deck."),
 ninja("63004", "Ninja Vanish", "give her a tough status card and shuffle this card into the [[Ninja]] deck."),
 carte("63005", "Ally", "* Daredevil", {"Cost": "3", "RES": "G", "HP": "3", "ATK": "2*", "THW": "2*", "Class": "Hero", "MaxPerDeck": "1"},
       ["DEFENDER", "MARTIAL ARTIST"], H,
       "[star] <b>Response</b>: After Daredevil uses a basic power, place a card from the encounter discard pile on top of the encounter deck.", "Matt Murdock"),
 carte("63006", "Event", "Acrobatic Prowess", {"Cost": "1", "RES": "Y", "Class": "Hero", "MaxPerDeck": "2"}, ["ACROBATIC", "SKILL"], H,
       "<b>Hero Action</b>: Ready Elektra and give her 1 facedown boost card."),
 carte("63007", "Event", "Killer Blow", {"Cost": "2", "RES": "Y", "Class": "Hero", "MaxPerDeck": "2"}, ["ATTACK"], H,
       "<b>Hero Action</b> <i>(attack)</i>: Deal up to 5 damage to an enemy. If this attack defeats that enemy, shuffle the top card of the [[Ninja]] deck into the encounter deck."),
 carte("63008", "Event", "Move Unseen", {"Cost": "2", "RES": "B", "Class": "Hero", "MaxPerDeck": "2"}, ["ACROBATIC", "THWART"], H,
       "<b>Hero Action</b> <i>(thwart)</i>: Remove up to 4 threat from a scheme. Shuffle the top card of the [[Ninja]] deck into the encounter deck."),
 carte("63009", "Event", "Sai Strike", {"Cost": "1", "RES": "R", "Class": "Hero", "MaxPerDeck": "2"}, ["ATTACK"], H,
       "<b>Hero Action</b> <i>(attack)</i>: Deal 3 damage to an enemy. For each Elektra's Sai you control, shuffle the top card of the [[Ninja]] deck into the encounter deck."),
 carte("63010", "Support", "* Resurrection Altar", {"Cost": "1", "RES": "B", "Class": "Hero", "MaxPerDeck": "1"}, ["HAND", "LOCATION"], H,
       "<b>Interrupt</b>: When you would be defeated, remove this card from the game → set your hit point dial to 9 instead. Find your obligation and reveal it."),
 carte("63011", "Support", "* White Tiger", {"Cost": "1", "RES": "B", "Class": "Hero", "MaxPerDeck": "1"}, ["PERSONA"], H,
       "<b>Response</b>: After you change to hero form, shuffle the top card of the [[Ninja]] deck into the encounter deck. Otherwise, give Elektra 1 facedown boost card."),
 carte("63012", "Upgrade", "Elektra's Sai", {"Cost": "2", "RES": "R", "Class": "Hero", "MaxPerDeck": "2", "Restricted": "1"}, ["WEAPON"], H,
       "Restricted. <i>(Max 2 restricted cards per player.)</i>\n<b>Hero Action</b>: Exhaust Elektra's Sai → deal 1 damage to an enemy and reduce the cost of the next [[Acrobatic]] or [[Attack]] event you play this phase by 1."),
 carte("63013", "Upgrade", "History with the Hand", {"Cost": "0", "RES": "B", "Class": "Hero", "MaxPerDeck": "1"}, ["CONDITION"], H,
       "Prerequisite (hero form).\nYou get +1 hand size.\n<b>Forced Response</b>: After you change form, discard this card."),
 carte("63014", "Upgrade", "Stealth Mastery", {"Cost": "1", "RES": "Y", "Class": "Hero", "MaxPerDeck": "1"}, ["SKILL"], H,
       "<b>Forced Interrupt</b>: When you attack or are attacked, choose to either increase or reduce the damage that attack deals by 3. Put Stealth Mastery on top of your deck."),
]
i = next(k for k, c in enumerate(liste) if c.get("card_id") == "63015")
liste[i:i] = neuf
open(P, "w", encoding="utf-8").write(json.dumps(d, indent=1, ensure_ascii=False) + "\n")
print(len(neuf), "cartes inserees avant l'index", i)
