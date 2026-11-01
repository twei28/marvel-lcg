#!/usr/bin/env python3
"""Genere les donnees du scenario 3 « Black Queen » (Selene) de Hellfire Hunt (Dipsome), prefixe `hf`, pack hellfire_hunt_black_queen (set 243)
+ le module Darkhold (hf361-hf366, porte ICI).

Idempotent. cards.json, sets_info.json sont reecrits en RELECTURE-MODIFICATION sous flock (d'autres agents editent les memes fichiers) : seules
MES cles sont touchees.
Usage : python3 generer_donnees.py <racine_moteur> <dossier_zip_extrait>
"""
import fcntl
import io
import json
import os
import sys

RACINE = sys.argv[1]
ZIP = sys.argv[2]  # .../Hellfire Hunt Campaign
PACK = "hellfire_hunt_black_queen"
AUTEUR = "Dipsome"
CLE_SET = "243. Custom (Hellfire Hunt - Black Queen)"

BQ, DK = "Black Queen", "Darkhold"


def carte(cid, typ, nom, set_name, desc, traits, text, **extra):
    c = {"card_id": cid, "type": typ, "name": nom, "subtitle": "", "desc": desc, "traits": traits,
         "set_name": set_name, "text": text, "custom": AUTEUR}
    c.update(extra)
    return c


CARTES = []
A = CARTES.append

# ============================================================ SET « Black Queen » (hf401-hf422 : numero du scan + 400)
SELENE_FR = ("<b>Forced Response</b>: After Selene attacks, heal damage from her equal to the amount of non-excess damage characters the "
             "defending player controlled took from this attack.")
A(carte("hf401", "Villain", "* Selene", BQ, {"HP": "12*", "ATK": "1", "SCH": "2", "Stage": "1"}, ["HELLFIRE", "MYSTIC"],
        SELENE_FR + "\n<i>\"Through all the centuries... I've never had anyone track me - when I didn't want them to. Unfortunately, you won't be "
        "alive long enough to share what you've learned...\"</i>"))
A(carte("hf402", "Villain", "* Selene", BQ, {"HP": "14*", "ATK": "2", "SCH": "2", "Stage": "2", "Toughness": "1"}, ["HELLFIRE", "MYSTIC"],
        "Toughness.\n" + SELENE_FR + "\n<i>\"Countless thousands have gone to the fire in my name. Which of you two... will be the next?\"</i>"))
A(carte("hf403", "Villain", "* Selene", BQ, {"HP": "17*", "ATK": "3", "SCH": "2", "Stage": "3", "Steady": "1", "Toughness": "1"}, ["HELLFIRE", "MYSTIC"],
        "Steady. Toughness.\n" + SELENE_FR + "\n<i>\"This is where I become a god.\"</i>"))

A(carte("hf404a", "MainScheme", "Throne of the Hellfire Club", BQ, {"Stage": "1"}, [],
        "<i>After Sebastian lost interest in the Club, Selene tried to reform the Inner Circle with demonic help, bringing Mephisto's son "
        "Blackheart in as her new Black King.</i>\n"
        "<b>Contents</b>: Selene (I) and Selene (II). <i>(Selene (II) and Selene (III) instead for expert mode.)</i> Black Queen, Darkhold and "
        "Standard encounter sets. One modular encounter set <i>(Hellfire Conclave)</i>.\n"
        "<b>Setup</b>: Put Under the Moonlight environment into the play. Set the Darkhold module aside. Shuffle the set-aside Darkhold Dwarf "
        "into the encounter deck."))
A(carte("hf404b", "MainScheme", "Throne of the Hellfire Club", BQ, {"StartingThreat": "1*", "TargetThreat": "5*", "EscalationThreat": "2*", "Stage": "1"}, [],
        "<i>After getting the throne, Black Queen sought some kind of helpful power to consolidate her position.</i>\n"
        "<b>Forced Interrupt</b>: When Darkhold Dwarf enters the discard pile, advance to stage 2A.\n"
        "<b>When Completed</b>: Give Selene a tough status card. If Beneath the Sun environment is in play, remove 2[per_hero] time counters from it."))
A(carte("hf405a", "MainScheme", "The Power of the Darkhold", BQ, {"Stage": "2"}, [],
        "<i>Selene sought to acquire the ancient Chthon Scrolls as known as the Darkhold, a book of evil spells. By tapping into the Darkhold's "
        "forbidden knowledge, Selene could unlock powerful spells and rituals to achieve her ultimate goal of godhood.</i>\n"
        "<b>When Revealed</b>: Shuffle the set-aside Darkhold modular set into the encounter deck."))
A(carte("hf405b", "MainScheme", "Get the Power", BQ, {"StartingThreat": "2*", "TargetThreat": "7*", "EscalationThreat": "1*", "Stage": "2"}, [],
        "<b>When Completed</b>: Give Selene a tough status card. Find Darkhold and attach it to Selene."))
A(carte("hf406a", "MainScheme", "Ascending to Godhood", BQ, {"Stage": "3"}, [],
        "<i>With the Darkhold's power under her control, Selene was able to perform a dark ritual to empowered herself for absorbing the life "
        "force of millions creatures to ascend to godhood.</i>\n"
        "<b>When Revealed</b>: Find the Immortal Moon Goddess side scheme and reveal it. Find Blackheart and put it into play engaged with the "
        "first player. <i>(Shuffle.)</i>"))
A(carte("hf406b", "MainScheme", "Ascending to Godhood", BQ, {"StartingThreat": "0", "TargetThreat": "17*", "EscalationThreat": "2*", "Stage": "3"}, [],
        "[star] <b>Forced Response</b>: After step one of the villain phase, place 1 threat here for each time counter on Under the Moonlight or "
        "Beneath the Sun.\n<b>If this stage is completed, the players lose the game.</b>"))

TIME_KO = "If there are no time counters here, flip this card."
RESP_TEMPS = ("<b>Forced Response</b>: After a character uses a basic power or an enemy activates, remove 1 time counter here.")
A(carte("hf407a", "Environment", "Under the Moonlight", BQ, {}, [],
        "Under the Moonlight enters play with 3[per_hero] time counters. " + TIME_KO + "\n"
        "<b>Forced Interrupt</b>: When Black Queen would activate, give her 1 more boost card.\n" + RESP_TEMPS))
A(carte("hf407b", "Environment", "Beneath the Sun", BQ, {}, [],
        "Beneath the Sun enters play with 3[per_hero] time counters. " + TIME_KO + "\n"
        "Each identity gets +1 to each of its basic powers.\n" + RESP_TEMPS))

A(carte("hf408", "Minion", "* Blackheart", BQ, {"HP": "9", "ATK": "3", "SCH": "1", "Boost": "3", "Guard": "1", "Patrol": "1", "Steady": "1"},
        ["DEMON", "ELITE"],
        "Guard. Patrol. Steady.\n<i>\"You've brought Hell to Earth!\"</i>\n<hr />\n"
        "[star] <b>Boost</b>: If this activation is an attack, this attack gains overkill, piercing, and ranged."))
for scan in (9, 10, 11, 12):
    A(carte("hf4%02d" % scan, "Minion", "Little Demon", BQ, {"HP": "3", "ATK": "2", "SCH": "1", "Boost": "2", "Patrol": "1", "Teamwork": "DEMON"},
            ["DEMON", "HELL"],
            "Patrol. Teamwork ([[Demon]]).\n<b>Forced Response</b>: After Little Demon attacks and damages you, you are confused."))
for scan in (13, 14, 15):
    A(carte("hf4%02d" % scan, "Attachment", "Hyponotic Trance", BQ, {"THW+": "-1", "Boost": "1"}, ["PSIONIC", "SKILL"],
            "Attached character cannot attack Selene and cannot defend against Selene's attacks.\n"
            "<b>When Revealed</b>: Attach to the ally with the highest remaining hit-point without Hyponotic Trance attached. Otherwise, this "
            "card gains surge.\n"
            "<b>Hero Action</b>: Spend [mental][mental] resources and remove 1 time counter from Beneath the Sun → discard this card."))
for scan in (16, 17):
    A(carte("hf4%02d" % scan, "Attachment", "Shining Shield", BQ, {}, ["PSIONIC", "SKILL"],
            "Attach to Selene.\nSelene cannot take more than 2 damage from a single attack.\n"
            "<b>Hero Action</b>: Spend a [energy] resource and remove 1 time counter from Beneath the Sun → discard this card.\n<hr />\n"
            "[star] <b>Boost</b>: Attach this card to Selene."))
A(carte("hf418", "Attachment", "Relentless Pursuit", BQ, {"Boost": "3"}, ["CONDITION"],
        "Attach to your identity.\n<b>Forced Interrupt</b>: When Selene would scheme against you, she attacks you instead.\n"
        "<b>Hero Action</b>: Spend a [physical] resource and remove 1 time counter from Beneath the Sun → discard this card."))
A(carte("hf419", "Treachery", "Dark Temptation", BQ, {"Boost": "1"}, [],
        "<b>When Revealed</b>: Selene attacks you.\n<hr />\n[star] <b>Boost</b>: If this attack defeats an ally, place 2 threat on the main scheme."))
A(carte("hf420", "Treachery", "Lunar Eclipse", BQ, {"Boost": "1"}, ["SPELL"],
        "<b>When Revealed</b>: Remove 1[per_hero] time counter from Beneath the Sun. If you cannot, place 1[per_hero] time counter on Under the "
        "Moonlight.\n<hr />\n[star] <b>Boost</b>: Reveal this card."))
A(carte("hf421", "SideScheme", "Eternal Night", BQ, {"StartingThreat": "3", "Boost": "3"}, [],
        "Time counter on Under the Moonlight environment could not be removed.\n<b>When Revealed</b>: Flip Beneath the Sun."))
A(carte("hf422", "SideScheme", "Immortal Moon Goddess", BQ, {"StartingThreat": "7", "Hinder": "2*", "Victory": "1", "Acceleration": "1", "Boost": "1"}, [],
        "<i>\"Soon...the world will know True External High Lords for the first time. Immortal. Invulnerable...and unstoppable.\"</i>\n"
        "Hinder 2[per_hero]. Victory 1.\nWhile Under the Moonlight is in play, Black Queen cannot be defeated."))

# ============================================================ MODULE « Darkhold » (hf361-hf366 : numero du scan + 360)
A(carte("hf361", "Minion", "* Darkhold Dwarf", DK, {"HP": "3", "ATK": "1", "SCH": "3", "Boost": "2"}, ["DEMON", "ELITE"],
        "<b>When Revealed</b>: Tuck the topmost [[Spell of Darkhold]] encounter card from the encounter discard pile under here.\n"
        "<b>When Defeated</b>: Reveal the card tucked here.\n<i>\"For ease of reference, call me what most people I meet do: The Darkhold Dwarf. "
        "Insensitive, I admit, but at my age, frankly, I don't give a damn.\"</i>"))
A(carte("hf362", "Attachment", "* Darkhold", DK, {"ATK+": "1", "Boost": "3", "Uses": "2,darkspell"}, ["MAGICAL BOOK"],
        "Attach to the villain.\nUses (2 darkspell counters)\n[star] <b>Forced Interrupt</b>: When the villain attacks, remove 1 Darkspell "
        "counter from here → give the attached character 1 additional boost card for this activation."))
A(carte("hf363", "Attachment", "Eternal Manipulation", DK, {"ATK+": "1", "Boost": "1"}, ["SPELL", "SPELL OF DARKHOLD"],
        "Treat attached ally as a minion with a blank text box <i>(except for [[TRAITS]])</i>. Attach minion's SCH is equal to its printed THW "
        "and it does not take consequential damage.\n"
        "<b>When Revealed</b>: If Darkhold is attached to the villain, attached this to your ally with highest hit-point, Remove 1 darkspell "
        "counter from Darkhold. Otherwise, find Darkhold attachment and reveal it."))
A(carte("hf364", "Treachery", "Hellfire Conjuration", DK, {"Boost": "1"}, ["SPELL", "SPELL OF DARKHOLD"],
        "<b>When Revealed</b>: If Darkhold is attached to the villain, take 3 indirect damages, remove 1 darkspell counter from Darkhold. "
        "Otherwise, find Darkhold attachment and reveal it."))
A(carte("hf365", "Treachery", "Soul Siphon", DK, {}, ["SPELL", "SPELL OF DARKHOLD"],
        "<b>When Revealed</b>: If Darkhold is attached to the villain, you are stunned and confused, remove 1 darkspell counter from Darkhold. "
        "Otherwise, find Darkhold and reveal it.\n<hr />\n[star] <b>Boost</b>: Reveal this card."))
A(carte("hf366", "Treachery", "Dimensional Portal", DK, {"Boost": "2"}, ["SPELL", "SPELL OF DARKHOLD"],
        "<b>When Revealed</b>: If Darkhold is attached to the villain, discard cards from the top of the encounter deck until a minion, reveal "
        "that minion, and remove 1 darkspell counter from Darkhold. Otherwise, find Darkhold and reveal it."))

CARTES.sort(key=lambda c: c["card_id"])

# ============================================================ ensembles de rencontre et scenario
# Black Queen : tout sauf villain, complots et environnement (mis en jeu / de cote par la mise en place).
ENS_BQ = ["hf408", "hf409", "hf410", "hf411", "hf412", "hf413", "hf414", "hf415", "hf416", "hf417", "hf418", "hf419", "hf420", "hf421", "hf422"]
ENS_DK = ["hf361", "hf362", "hf363", "hf364", "hf365", "hf366"]
ENSEMBLES = {"hf_black_queen": ("Black Queen", ENS_BQ), "hf_darkhold": ("Darkhold", ENS_DK)}


def scenario(expert):
    return {"version": "0.5.8", "name": "Black Queen",
            "villain": (["hf402", "hf403"] if expert else ["hf401", "hf402"]),
            "expert": expert,
            "schemes": ["hf404a,hf404b", "hf405a,hf405b", "hf406a,hf406b"],
            "set_aside": ["hf407a,hf407b"],
            "encounters": [],
            "encounter_sets": ["hf_black_queen", "hf_darkhold", "standard"] + (["expert"] if expert else []),
            "modular_sets": ["hf_hellfire_conclave"]}


# ============================================================ images : numero du scan -> card_id
IMG = {}
for n in (1, 2, 3):
    IMG["Scenario/Black Queen/%d.png" % n] = "hf40%d" % n
for n in (4, 5, 6, 7):
    IMG["Scenario/Black Queen/%da.png" % n] = "hf40%da" % n
    IMG["Scenario/Black Queen/%db.png" % n] = "hf40%db" % n
for n in range(8, 23):
    IMG["Scenario/Black Queen/%d.png" % n] = ("hf4%02d" % n)
for n in range(1, 7):
    IMG["Modules/darkhold/%d.png" % n] = "hf36%d" % n
LANDSCAPE = {"hf404a", "hf404b", "hf405a", "hf405b", "hf406a", "hf406b", "hf421", "hf422"}


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
    for e in ENSEMBLES.values():
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
        sets[CLE_SET] = {"name": PACK, "scenarios": ["hellfire_black_queen"], "heroes": [],
                         "encounters": list(ENSEMBLES), "max_id": CARTES[-1]["card_id"]}
        ecrire(p, sets, 1)

    for cle, (nom, lst) in ENSEMBLES.items():
        ecrire(os.path.join(RACINE, "data", "encounter_sets", cle + ".json"), {"version": "0.5.8", "name": nom, "encounters": lst}, 2)
    ecrire(os.path.join(RACINE, "data", "scenarios", "hellfire_black_queen.json"), scenario(False), 2)
    ecrire(os.path.join(RACINE, "data", "scenarios", "hellfire_black_queen_expert.json"), scenario(True), 2)

    from PIL import Image
    cible = os.path.join(RACINE, "assets", "pics")
    for rel, cid in IMG.items():
        src = os.path.join(ZIP, rel)
        im = Image.open(src).convert("RGB")
        taille = (882, 615) if cid in LANDSCAPE else (615, 882)
        assert (im.size[0] > im.size[1]) == (taille[0] > taille[1]), (rel, im.size)
        dst = os.path.join(cible, cid + ".jpg")
        if os.path.islink(dst):
            os.remove(dst)
        im.resize(taille, Image.LANCZOS).save(dst, "JPEG", quality=88)
    print("cartes", len(CARTES), "images", len(IMG))


main()
