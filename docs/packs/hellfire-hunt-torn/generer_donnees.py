#!/usr/bin/env python3
"""Genere les donnees du scenario 4 « Torn » de Hellfire Hunt (Dipsome), prefixe `hf`, pack `hellfire_hunt_torn` (set 244), ainsi que les
modules Negasonic Teenage Warhead (hf341-hf348) et Immensity (hf351-hf358), dont ce pack est responsable.

Idempotent. cards.json et sets_info.json sont relus et reecrits SOUS flock (/tmp/cards_json.lock) : seules NOS cles sont touchees.
Usage : python3 generer_donnees.py <racine_moteur> <dossier « Hellfire Hunt Campaign » extrait> [--sans-images]
"""
import fcntl
import io
import json
import os
import sys

RACINE = sys.argv[1]
ZIP = sys.argv[2]
SANS_IMAGES = "--sans-images" in sys.argv
PACK = "hellfire_hunt_torn"
AUTEUR = "Dipsome"
CLE_SET = "244. Custom (Hellfire Hunt - Torn)"
TN, NG, IM = "Torn", "Negasonic Teenage Warhead", "Immensity"


def carte(cid, typ, nom, set_name, desc, traits, text, **extra):
    c = {"card_id": cid, "type": typ, "name": nom, "subtitle": "", "desc": desc, "traits": traits,
         "set_name": set_name, "text": text, "custom": AUTEUR}
    c.update(extra)
    return c


CARTES = []
A = CARTES.append

# ============================================================ SCENARIO « Torn » (hf501-hf510 = 500 + numero n/10 du scan)
# Les images 1a/1b/2a/2b/3B/4/4b ... de mai 2025 sont les textes FINAUX ; a1/a2/b1/b2 (dec. 2024) et « 3b(1) » (oct. 2024) sont des etats anterieurs
# (textes differents) et ne sont PAS portes.
FLIP_PV = ("<b>Forced Response</b>: After the end of the villain phase, flip this card, then set Emma Frost's hit point dial to her printed "
           "hit points.")
INT_VAINCUE = ("<b>Forced Interrupt</b>: When Emma Frost would be defeated, remove 5 threat from each scheme in play, and flip this card instead.")
A(carte("hf501a", "Villain", "* Emma Frost", TN, {"HP": "7*", "ATK": "1*", "SCH": "2*", "Stage": "1"}, ["HELLFIRE", "PSIONIC", "X-MEN"],
        "[star] <b>Forced Response</b>: After Emma Frost activates, discard 1 card from the top of the encounter deck, if it has the [[Psionic]] "
        "trait, place 1 threat on each scheme.\n" + INT_VAINCUE))
A(carte("hf501b", "Villain", "* Emma Frost", TN, {"HP": "INF", "ATK": "0*", "SCH": "0*", "Stage": "1"}, ["HELLFIRE", "PSIONIC", "X-MEN"],
        "[star] <b>Forced Interrupt</b>: When Emma Frost would activate, discard 2 cards from the top of the encounter deck instead.\n" + FLIP_PV))
A(carte("hf502a", "Villain", "* Emma Frost", TN, {"HP": "8*", "ATK": "2*", "SCH": "2*", "Stage": "1"}, ["HELLFIRE", "PSIONIC", "X-MEN"],
        "[star] <b>Forced Response</b>: After Emma Frost activates, discard 2 cards from the top of the encounter deck, for each [[Psionic]] card "
        "discarded in this way, place 1 threat on each scheme.\n" + INT_VAINCUE))
A(carte("hf502b", "Villain", "* Emma Frost", TN, {"HP": "INF", "ATK": "0*", "SCH": "0*", "Stage": "1"}, ["HELLFIRE", "PSIONIC", "X-MEN"],
        "[star] <b>Forced Interrupt</b>: When Emma Frost activates against a player, give the player a facedown encounter card instead.\n" + FLIP_PV))

A(carte("hf503a", "MainScheme", "The Hellfire Club's Revenge", TN, {"Stage": "1"}, [],
        "<b>Contents</b>: Emma Frost (A1) <i>(Emma Frost (B1) instead for expert mode)</i>. Torn, Perfection and Standard encounter set.\n"
        "<b>Setup</b>: Choose 3 modular sets, each with an [[Elite]], [[Hellfire]] minion <i>(Recommended: Immensity, Sebastian Shaw, "
        "Negasonic Teenage Warhead)</i> and shuffle them into the encounter deck. Shuffle every [[Elite]], [[Hellfire]] minion to create the "
        "Hellfire deck and set it next to the encounter deck <i>(see insert)</i>. Put the Nova's Psychic Puppetry side scheme into play, "
        "[[Controlled]] side face up."))
A(carte("hf503b", "MainScheme", "Free Cassandra Nova", TN, {"StartingThreat": "1*", "TargetThreat": "15*", "EscalationThreat": "1*", "Stage": "1"}, [],
        "The players cannot win unless they help Emma Frost to escape Cassandra's control.\n"
        "<b>Forced Interrupt</b>: At the start of the player phase, in player order, each player not engaged with an [[Elite]], [[Hellfire]] "
        "minion reveals the top card of the Hellfire deck.\n<b>If this scheme is completed, the players lose the game.</b>"))
PUPPET_RESP = ("<b>Forced Response</b>: After an [[Elite]], [[Hellfire]] minion is defeated, remove 5 threat from another side scheme. "
               "Otherwise, remove 5 threat from here.")
A(carte("hf504a", "SideScheme", "Nova's Psychic Puppetry", TN, {"StartingThreat": "8", "Permanent": "1", "Hinder": "5*"}, ["CONTROLLED"],
        "Permanent. Hinder 5[per_hero].\n<b>Forced Interrupt</b>: When the last threat is removed from this scheme, discard each [[Hellfire]] "
        "minion in play and deal each player a facedown encounter card. Then, flip this card. <i>(The player can help Emma Frost to escape "
        "on that side.)</i>\n" + PUPPET_RESP))
A(carte("hf504b", "SideScheme", "Nova's Psychic Puppetry", TN, {"StartingThreat": "1", "Permanent": "1", "Hinder": "12*"}, ["FRAGMENT"],
        "Permanent. Hinder 12[per_hero].\nEach [[Hellfire]] minion gains the [[Illusion]] trait.\n<b>Forced Interrupt</b>: When the last threat "
        "is removed from this scheme, Emma Frost escapes from the control of Cassandra Nova, the players win the game.\n" + PUPPET_RESP))
A(carte("hf505", "Obligation", "Protect Students", TN, {"Boost": "2", "GiveTo": ""}, [],
        "Your hero gets -1 ATK, and -1 DEF.\n<b>Alter-Ego Action</b>: Exhaust your identity and reveal 1 card from the Hellfire deck → heal 1 "
        "damage from each friendly character in play. Discard this card."))
A(carte("hf506", "Obligation", "Uncover The Truth", TN, {"Boost": "2", "Hazard": "1", "GiveTo": ""}, [],
        "<b>Alter-Ego Action</b>: Exhaust your identity → heal 5 damage from the villain and remove 5 threat from a side scheme. Discard this "
        "obligation."))
A(carte("hf507", "SideScheme", "Psychic Bulwark", TN, {"Boost": "2", "StartingThreat": "9", "Victory": "1"}, ["PSIONIC"],
        "<i>Nova's psychic influence envelops her thralls, shielding them from harm as she weaves her twisted web.</i>\nVictory 1.\n"
        "Each minion gains guard and patrol.\n<hr />\n[star] <b>Boost</b>: Give each minion a tough status card."))
A(carte("hf508", "SideScheme", "Psychic Entanglement", TN, {"Boost": "2", "StartingThreat": "8", "Victory": "1"}, ["PSIONIC"],
        "<i>Frost's web of deceit and illusion ensnares the heroes, trapping them in a labyrinth of her own design.</i>\nVictory 1.\n"
        "Threat cannot be removed from other side schemes.\n<b>When Defeated</b>: Deal each player a facedown encounter card."))
A(carte("hf509", "SideScheme", "Psionic Paragon", TN, {"Boost": "2", "StartingThreat": "4*"}, ["PSIONIC"],
        "Emma Frost gets +10 hit point.\nEach [[Illusion]] card gains incite 1.\n<b>When Revealed</b>: Deal 1 facedown encounter card to each "
        "player with no engaged minions."))
A(carte("hf510", "SideScheme", "Hellfire Assault", TN, {"StartingThreat": "1*"}, [],
        "Threat cannot be removed from here except by thwarting.\n<b>Forced Response</b>: After a [[Hellfire]] minion is defeated by a player, "
        "if it is White Queen, Emma Frost attacks the player. Otherwise, Emma Frost schemes.\n<hr />\n[star] <b>Boost</b>: Reveal this card."))

# ============================================================ MODULE « Negasonic Teenage Warhead » (hf341-hf348 = 340 + numero du scan)
A(carte("hf341", "Minion", "* Negasonic Teenage Warhead", NG, {"HP": "4", "ATK": "2*", "SCH": "1", "Boost": "1", "Steady": "1", "Toughness": "1"},
        ["ELITE", "HELLFIRE"],
        "Steady. Toughness.\n[star] When Negasonic Teenage Warhead attacks you, you must exhaust a support or upgrade you control, if able.\n"
        "<hr />\n[star] <b>Boost</b>: Exhaust a support or upgrade you control."))
PERCEPTION = ("Attach to your identity.\nAttached character cannot be readied.\n<b>Alter-Ego Action</b>: Spend [mental][mental] → discard this "
              "card.\n<hr />\n[star] <b>Boost</b>: Change your form <i>(flip your identity card)</i>.")
for cid in ("hf342", "hf343"):
    A(carte(cid, "Attachment", "Perception Manipulation", NG, {}, ["ILLUSION", "PSIONIC"], PERCEPTION))
MIND = ("<b>When Revealed</b>: Reveal the topmost attachment in the encounter discard pile. Otherwise, this card gains surge.\n<hr />\n"
        "[star] <b>Boost</b>: Exhaust your hero.")
for cid in ("hf344", "hf345"):
    A(carte(cid, "Treachery", "Mind Over Matter", NG, {"Boost": "1"}, ["PSIONIC", "SKILL"], MIND))
MATTER = ("<b>When Revealed</b>: Discard a card you control, then search your deck and discard pile for a card of the same type but with a "
          "resource cost less than the resource cost of the discarded card, and put that card into play. Otherwise, this card gains surge.")
for cid in ("hf346", "hf347", "hf348"):
    A(carte(cid, "Treachery", "Matter Manipulation", NG, {"Boost": "2"}, ["PSIONIC", "SKILL"], MATTER))

# ============================================================ MODULE « Immensity » (hf351-hf358 = 350 + numero du scan)
A(carte("hf351", "Minion", "* Cassandra Nova", IM, {"HP": "2", "ATK": "3", "SCH": "3", "Steady": "1"}, ["ELITE", "HELLFIRE", "PSIONIC"],
        "Steady.\n<b>When Revealed</b>: Find the Cassandra's Telepathic Cloak attachment and put it into play.\n<hr />\n"
        "[star] <b>Boost</b>: Put Cassandra Nova into play engaged with you."))
A(carte("hf352", "Treachery", "Illusory Duty", IM, {"Boost": "2"}, ["ILLUSION", "PSIONIC"],
        "<b>When Revealed</b>: Discard 3 cards from the top of the encounter deck. Reveal each obligation discarded in this way. If no "
        "obligation was not revealed this way, search the encounter deck, discard pile, set-aside area, and removed-from-game area for a copy "
        "of your obligation, then reveal it and remove this card from the game."))
A(carte("hf353", "Treachery", "Mental Paralysis", IM, {"Boost": "3", "Surge": "1"}, ["PSIONIC", "SKILL"],
        "Surge.\n<b>When Revealed</b>: You are stunned and confused.\n<hr />\n[star] <b>Boost</b>: You are stunned and confused."))
A(carte("hf354", "Attachment", "Cassandra's Telepathic Cloak", IM, {"Boost": "1"}, ["ARTIFACT", "ITEM"],
        "Attach to Cassandra Nova. If she is not in play, find Cassandra Nova, reveal her, and then attach this card on her.\n"
        "Cassandra Nova cannot take any amount of damage.\n<b>Forced Response</b>: After Cassandra Nova attacks you, discard this card."))
JUMP = ("Attach to the highest hit-point minion. Otherwise, this gains surge.\n[star] <b>Forced Interrupt</b>: When the attached character attacks "
        "you, give them 1 additional boost card for this activation.\n<hr />\n[star] <b>Boost</b>: Deal yourself 1 facedown encounter card.")
for cid in ("hf355", "hf356"):
    A(carte(cid, "Attachment", "Jumpstart", IM, {"SCH+": "2", "ATK+": "0*"}, ["CONDITION"], JUMP))
for cid in ("hf357", "hf358"):
    A(carte(cid, "Obligation", "Narrow Minded", IM, {"Boost": "2", "Amplify": "1", "GiveTo": ""}, ["ILLUSION", "PSIONIC"],
            "<b>Alter-Ego Action</b>: Exhaust your identity → discard this card."))

# ============================================================ ensembles de rencontre et scenarios
ENS = {"hf_torn": ("Torn", ["hf505", "hf506", "hf507", "hf508", "hf509", "hf510"]),
       "hf_negasonic_teenage_warhead": ("Negasonic Teenage Warhead", ["hf34%d" % i for i in range(1, 9)]),
       "hf_immensity": ("Immensity", ["hf35%d" % i for i in range(1, 9)])}
MODULAIRES = ["hf_sebastian_shaw", "hf_negasonic_teenage_warhead", "hf_immensity"]


def scenario(expert, racine):
    modulaires = [m for m in MODULAIRES if m in ENS or os.path.exists(os.path.join(racine, "data", "encounter_sets", m + ".json"))]
    return {"version": "0.5.8", "name": "Torn",
            "villain": ["hf502a,hf502b"] if expert else ["hf501a,hf501b"],
            "expert": expert,
            "schemes": ["hf503a,hf503b"],
            "set_aside": ["hf504a,hf504b"],
            "encounters": [],
            "encounter_sets": ["hf_torn", "hf_perfection", "standard"] + (["expert"] if expert else []),
            "modular_sets": modulaires}


# ============================================================ images : fichier source -> card_id
IMG = {"Scenario/Torn/1a.png": "hf501a", "Scenario/Torn/2a.png": "hf501b", "Scenario/Torn/1b.png": "hf502a", "Scenario/Torn/2b.png": "hf502b",
       "Scenario/Torn/3.png": "hf503a", "Scenario/Torn/3B.png": "hf503b", "Scenario/Torn/4.png": "hf504a", "Scenario/Torn/4b.png": "hf504b"}
for n in range(5, 11):
    IMG["Scenario/Torn/%d.png" % n] = "hf5%02d" % n
for n in range(1, 9):
    IMG["Modules/Negasonic Teenager Warhead/%d.png" % n] = "hf34%d" % n
    IMG["Modules/Immensity/%d.png" % n] = "hf35%d" % n
PETIT_COTE = 615


def lire(chemin):
    return json.load(io.open(chemin, encoding="utf-8", newline=""))


def ecrire(chemin, obj, indent):
    with io.open(chemin, "w", encoding="utf-8", newline="") as f:
        f.write(json.dumps(obj, indent=indent, ensure_ascii=False))


class Verrou:
    def __enter__(self):
        self.f = open("/tmp/cards_json.lock", "w")
        fcntl.flock(self.f, fcntl.LOCK_EX)

    def __exit__(self, *a):
        fcntl.flock(self.f, fcntl.LOCK_UN)
        self.f.close()


def main():
    ids = [c["card_id"] for c in CARTES]
    assert len(ids) == len(set(ids)), "card_id en double"
    for e in ENS.values():
        for i in e[1]:
            assert i in ids, i
    with Verrou():
        p = os.path.join(RACINE, "data", "cards.json")
        cartes = lire(p)
        for k, v in cartes.items():
            if k != PACK and isinstance(v, list):
                assert not ({c.get("card_id") for c in v if isinstance(c, dict)} & set(ids)), "collision avec le pack %s" % k
        cartes[PACK] = CARTES
        ecrire(p, cartes, 1)

        p = os.path.join(RACINE, "data", "sets_info.json")
        sets = lire(p)
        for k in list(sets):
            if isinstance(sets[k], dict) and sets[k].get("name") == PACK and k != CLE_SET:
                del sets[k]
        sets[CLE_SET] = {"name": PACK, "scenarios": ["hellfire_torn"], "heroes": [], "encounters": list(ENS), "max_id": "hf510"}
        ecrire(p, sets, 1)

        # Le prefixe `hf` est DEJA declare (pack hellfire_hunt_white_queen) : les packs des autres scenarios et les fondations (set 241)
        # cohabitent sans entree de plus (tools/verifier_prefixes.py ne regarde que le prefixe).

        for cle, (nom, lst) in ENS.items():
            ecrire(os.path.join(RACINE, "data", "encounter_sets", cle + ".json"), {"version": "0.5.8", "name": nom, "encounters": lst}, 2)
        ecrire(os.path.join(RACINE, "data", "scenarios", "hellfire_torn.json"), scenario(False, RACINE), 2)
        ecrire(os.path.join(RACINE, "data", "scenarios", "hellfire_torn_expert.json"), scenario(True, RACINE), 2)

    if not SANS_IMAGES:
        from PIL import Image
        cible = os.path.join(RACINE, "assets", "pics")
        for rel, cid in IMG.items():
            im = Image.open(os.path.join(ZIP, rel)).convert("RGB")
            w, h = im.size
            f = PETIT_COTE / min(w, h)
            im = im.resize((max(1, round(w * f)), max(1, round(h * f))), Image.LANCZOS)
            dst = os.path.join(cible, cid + ".jpg")
            if os.path.islink(dst):
                os.remove(dst)
            im.save(dst, "JPEG", quality=88, optimize=True)
    print("cartes", len(CARTES), "images", 0 if SANS_IMAGES else len(IMG))


main()
