#!/usr/bin/env python3
"""Genere les donnees du scenario 2 « Black King » (Sebastian Shaw) de Hellfire Hunt (Dipsome), prefixe `hf`, pack
`hellfire_hunt_black_king`, set 242, plus le module « Sebastian Shaw » (hf331-hf338, que ce scenario porte seul).

Idempotent. cards.json et sets_info.json sont relus-modifies-ecrits sous flock (un autre agent edite les memes fichiers) :
ne touche QUE la cle de notre pack et NOTRE cle de set.
Usage : python3 generer_donnees.py <racine_moteur> <dossier_zip_extrait> [--sans-images]
"""
import fcntl
import io
import json
import os
import sys

RACINE = sys.argv[1]
ZIP = sys.argv[2]  # .../Hellfire Hunt Campaign
PACK = "hellfire_hunt_black_king"
AUTEUR = "Dipsome"
CLE_SET = "242. Custom (Hellfire Hunt - Black King)"
BK, SS = "Black King", "Sebastian Shaw"


def carte(cid, typ, nom, set_name, desc, traits, text, **extra):
    c = {"card_id": cid, "type": typ, "name": nom, "subtitle": "", "desc": desc, "traits": traits,
         "set_name": set_name, "text": text, "custom": AUTEUR}
    c.update(extra)
    return c


CARTES = []
A = CARTES.append

# ============================================================ SET « Black King » (hf201-hf227)
ABS_TXT = ("[star] <b>Forced Interrupt</b>: When Sebastian Shaw attacks, remove all energy counters here to a maximum of 3. For each energy "
           "counter removed in this way, he gets +1 ATK for this activation.\n<i>Absorb</i> — <b>Forced Response</b>: After Sebastian Shaw "
           "takes damage from an attack, place energy counters on him equal to the damage taken.")
A(carte("hf201", "Villain", "* Sebastian Shaw", BK, {"HP": "13*", "ATK": "0*", "SCH": "2", "Stage": "1"}, ["HELLFIRE"], ABS_TXT))
A(carte("hf202", "Villain", "* Sebastian Shaw", BK, {"HP": "15*", "ATK": "1*", "SCH": "3", "Stage": "2"}, ["HELLFIRE"], ABS_TXT))
A(carte("hf203", "Villain", "* Sebastian Shaw", BK, {"HP": "17*", "ATK": "1*", "SCH": "3", "Stage": "3"}, ["HELLFIRE"],
        ABS_TXT + " Place 1 additional energy counter here."))

A(carte("hf204a", "MainScheme", "Jailbreak at the Hellfire Club", BK, {"Stage": "1"}, [],
        "<i>The Hellfire Club has kidnapped a group of powerful mutants, the heroes is going to infiltrate the Hellfire Club's stronghold and "
        "stage a daring rescue mission.</i>\n"
        "<b>Contents</b>: Sebastian Shaw (I) and Sebastian Shaw (II). <i>(Sebastian Shaw (II) Sebastian Shawing (III) instead for expert mode.)</i> "
        "Black King, Sebastian Shaw and Standard encounter sets. One modular encounter set <i>(Hellfire Conclave)</i>.\n"
        "<b>Setup</b>: Remove each minion named Sebastian Shaw from the game. Set each [[Captive]] ally aside. Reveal the Captured by Hellfire! "
        "side scheme. Attach Black King to Sebastian Shaw."))
A(carte("hf204b", "MainScheme", "Jailbreak at the Hellfire Club", BK,
        {"StartingThreat": "0", "TargetThreat": "5*", "EscalationThreat": "1*", "Stage": "1"}, [],
        "Threat cannot be removed from this scheme.\n<b>Forced Interrupt</b>: When Sebastian Shaw would scheme against you, deal you 1 "
        "facedown encounter card instead.\n<b>If this stage is completed, the players lose the game.</b>"))
A(carte("hf205a", "MainScheme", "Operation Hellfire Ascendant", BK, {"Stage": "2"}, [],
        "<i>Shaw is consolidating his power and implementing his vision of a Hellfire-controlled society.</i>\n"
        "<b>When Revealed</b>: Deal each player a facedown encounter card. Flip Black King attachment."))
A(carte("hf205b", "MainScheme", "Operation Hellfire Ascendant", BK,
        {"StartingThreat": "4*", "TargetThreat": "13*", "EscalationThreat": "1*", "Stage": "2"}, [],
        "<i>The mutant captives are merely bait for the heroes, and Shaw has set his sights on the rescuers. He's angry but is also waiting for "
        "the chance to fight you.</i>\n<b>Hero Action</b>: Exhaust a [[Captive]] ally you control → remove 2 energy counters from Sebastian Shaw. "
        "<i>(Limit once per round per player.)</i>\n<b>If this stage is completed, the players lose the game.</b>"))

A(carte("hf206", "SideScheme", "Captured by Hellfire!", BK, {"StartingThreat": "5", "Victory": "1", "Permanent": "1"}, [],
        "Permanent. Victory 1.\n<b>When Revealed</b>: Place 1[per_hero] random set-aside [[Captive]] allies facedown beneath this scheme.\n"
        "<b>When Defeated</b>: The player who defeated this scheme takes a random card from beneath here, and add it to their hand. After that, "
        "if there still has card under this scheme, place 5 threat here. Otherwise, advance to main scheme 2A and add this card to the victory display."))

A(carte("hf207a", "Attachment", "* Black King", BK, {"Permanent": "1"}, ["TITLE"],
        "Permanent.\n<i>King's Tactic</i> — <b>Forced Interrupt</b>: When Sebastian Shaw's \"<i>Absorb</i>\" ability triggers while there is an "
        "energy counter on him, remove each energy counters from him, place that much threat on the main scheme."))
A(carte("hf207b", "Attachment", "\"And What Is Theirs... Is Mine.\"", BK, {"Permanent": "1"}, ["TITLE"],
        "Permanent.\nSebastian Shaw gains stalwart while there is more than 5 energy counters on him.\n<i>King's Tactic</i> — "
        "<b>Forced Interrupt</b>: When Sebastian Shaw's \"<i>Absorb</i>\" ability triggers while there is an energy counter on him, remove each "
        "energy counters from him, place that much threat on the main scheme. <i>(Max 1[per_hero] times per round.)</i>"))

A(carte("hf208", "Ally", "* Dust", BK, {"Cost": "2", "HP": "3", "ATK": "2**", "THW": "2*", "RES": "R", "Class": "Campaign;Basic"},
        ["CAPTIVE", "MUTANT"],
        "[star] <b>Interrupt</b>: When Dust attacks, resolve this attack against the villain and each minion engaged with you.\n"
        "<i>\"Be silent! No God would condone such horror! Such hatred! You are the abomination! \"</i>", subtitle="Sooraya Qadir"))
A(carte("hf209", "Ally", "* Mercury", BK, {"Cost": "2", "HP": "5", "ATK": "2***", "THW": "2***", "RES": "B", "Toughness": "1", "Class": "Campaign;Basic"},
        ["CAPTIVE", "MUTANT"], "Toughness.\n<i>\"Worst...field trip...ever!\"</i>", subtitle="Cessily Kincaid"))
A(carte("hf210", "Ally", "* Surge", BK, {"Cost": "2", "HP": "2", "ATK": "1*", "THW": "2*", "RES": "Y", "Class": "Campaign;Basic"},
        ["CAPTIVE", "MUTANT"], "[star] <b>Interrupt</b>: When Surge attacks an enemy, that enemy get stunned.\n"
        "<i>\"We split the youth vote, didn't we?\"</i>", subtitle="Noriko Ashida"))
A(carte("hf211", "Ally", "* Prodigy", BK, {"Cost": "1", "HP": "1", "ATK": "1*", "THW": "1*", "RES": "G", "Class": "Campaign;Basic"},
        ["CAPTIVE", "MUTANT"], "<b>Response</b>: After you play Prodigy from hand, draw 1 card.\n"
        "<i>\"There are fates worse than death. And sometimes your own imagination is more monstrous than the truth.\"</i>", subtitle="David Alleyne"))

for n in (12, 13, 14, 15):
    A(carte("hf2%d" % n, "Minion", "Ebon Knight", BK, {"HP": "2", "ATK": "2", "SCH": "2", "Boost": "1", "Guard": "1", "Patrol": "1", "Quickstrike": "1"},
            ["HELLFIRE"], "Guard. Patrol. Quickstrike.\n<hr />\n[star] <b>Boost</b>: After this activation, deal Ebon Knight to you as a "
            "facedown encounter card."))
for n in (16, 17):
    A(carte("hf2%d" % n, "Attachment", "Inhibitor Collar", BK, {"Boost": "2"}, ["TECH", "ARTIFACT"],
            "Attach to your identity.\nTreat your identity's printed text box as blank <i>(except for [[TRAITS]])</i>.\n"
            "<b>Alter-Ego Action</b>: Spend [physical][physical] resources → discard this card. Any player may trigger this ability.\n<hr />\n"
            "[star] <b>Boost</b>: If this activation is an attack, this attack gains overkill."))
for n in (18, 19):
    A(carte("hf2%d" % n, "Attachment", "Targeted by Hellfire", BK, {"Boost": "3"}, ["CONDITION"],
            "Attach to your identity if a copy of Targeted by Hellfire is not attached to you. Otherwise, this card gains surge.\n"
            "<b>Forced Response</b>: After you change to hero form, Sebastian Shaw and each [[Hellfire]] minion engaged with you attacks you. "
            "Discard this card."))
for n in (20, 21):
    A(carte("hf2%d" % n, "Treachery", "Mutant Suppression", BK, {"Boost": "1"}, ["TACTIC"],
            "<b>When Revealed</b>: Exhaust your identity and each ally you control.\n<hr />\n"
            "[star] <b>Boost</b>: After this activation, exhaust your identity and place 1 energy counter on Sebastian Shaw."))
for n in (22, 23):
    A(carte("hf2%d" % n, "Treachery", "Hellfire Indoctrination", BK, {"Boost": "1"}, ["HELLFIRE", "TACTIC"],
            "<b>When Revealed</b>: Confuse each ally you control. If there is no [[Captive]] ally is confused in this way, this gains surge.\n<hr />\n"
            "[star] <b>Boost</b>: After this activation, place 2 energy counters on Sebastian Shaw."))
for n in (24, 25):
    A(carte("hf2%d" % n, "Treachery", "Energic Backlash", BK, {"Boost": "1"}, ["SKILL"],
            "<b>When Revealed (Alter-Ego)</b>: Place 4 energy counters on Sebastian Shaw.\n<b>When Revealed (Hero)</b>: Place 2 energy counters "
            "on Sebastian Shaw. Sebastian Shaw attacks you.\n<hr />\n[star] <b>Boost</b>: After this activation, place 3 energy counters on "
            "Sebastian Shaw."))
A(carte("hf226", "SideScheme", "Mutant Experimentation", BK, {"StartingThreat": "3*", "Boost": "2", "Hazard": "1"}, [],
        "<i>In their quest for power, the Hellfire Club has subjected the captured mutants to invasive experiments designed to unlock their full "
        "ptential for Shaw's personal army.</i>\n<b>When Defeated</b>: Each player must choose and discard 1 card from their hand."))
A(carte("hf227", "SideScheme", "Rage of Black King", BK, {"StartingThreat": "2", "Boost": "2", "Hinder": "1*"}, [],
        "<i>\"And remember... Failure is not an option.\"</i>\nHinder 1[per_hero].\n<b>Forced Response</b>: After Sebastian Shaw activates, he "
        "gains a tough status card.\n<b>When Defeated</b>: Each player chooses to either place 2 energy counters on Sebastian Shaw or deal "
        "themselves 1 facedown encounter card."))

# ============================================================ MODULE « Sebastian Shaw » (hf331-hf338)
A(carte("hf331", "Minion", "* Sebastian Shaw", SS, {"HP": "6", "ATK": "2", "SCH": "1", "Boost": "1", "Villainous": "1"}, ["ELITE", "HELLFIRE"],
        "Villainous.\n<b>Forced Response</b>: After Sebastian Shaw takes any amount of damage, place that amount of threat on the main scheme.\n"
        "<hr />\n[star] <b>Boost</b>: Give the villain a facedown boost card."))
for n in (32, 33):
    A(carte("hf3%d" % n, "Attachment", "Energy Absorption", SS, {"Boost": "2", "MaxPerUnit": "1"}, ["SUPERPOWER"],
            "Max 1 per character.\nAttach to Sebastian Shaw. Otherwise, attach to the villain.\n<b>Forced Interrupt</b>: When the attached "
            "character would take any amount of damage, heal that character for that amount instead of dealing damage. If no damage was healed "
            "this way, give that character a tough status card. Set aside this card."))
for n in (34, 35):
    A(carte("hf3%d" % n, "Attachment", "Energy Counterattack", SS, {"Boost": "2", "MaxPerUnit": "1"}, ["SUPERPOWER"],
            "Max 1 per character.\nAttach to Sebastian Shaw. Otherwise, attach to the villain.\n<b>Forced Interrupt</b>: When a character "
            "attacks the attached character, the attached character attacks that character. <i>(Resolve the attached character's attack "
            "first)</i>. Set aside this card."))
for n in (36, 37):
    A(carte("hf3%d" % n, "Treachery", "Ambient Energy Absorption", SS, {"Boost": "1"}, ["SKILL"],
            "<b>When Revealed</b>: Choose a set-aside Sebastian Shaw attachment and reveal it. Give this card to the enemy who attached that "
            "attachment as a facedown boost card. Otherwise, this card gains surge.\n<hr />\n"
            "[star] <b>Boost</b>: Give this enemy 1 additional boost card for this activation."))
A(carte("hf338", "SideScheme", "Hellfire Domination", SS, {"StartingThreat": "3*", "Boost": "3", "Amplify": "1"}, [],
        "<i>Sebastian Shaw sat in his throne, his cold, calculating gaze surveying the city below. A malicious grin spread across his lips as he "
        "contemplated his latest scheme.</i>\n<b>When Defeated</b>: Shuffle each set-aside Sebastian Shaw encounter card into the encounter deck."))

# ============================================================ ensembles de rencontre et scenario
ENS_BK = ["hf206", "hf212", "hf213", "hf214", "hf215", "hf216", "hf217", "hf218", "hf219", "hf220", "hf221", "hf222", "hf223", "hf224", "hf225",
          "hf226", "hf227"]
ENS_SS = ["hf331", "hf332", "hf333", "hf334", "hf335", "hf336", "hf337", "hf338"]
ENSEMBLES = {"hf_black_king": ("Black King", ENS_BK), "hf_sebastian_shaw": ("Sebastian Shaw", ENS_SS)}


def scenario(expert):
    return {"version": "0.5.8", "name": "Black King",
            "villain": (["hf202", "hf203"] if expert else ["hf201", "hf202"]),
            "expert": expert,
            "schemes": ["hf204a,hf204b", "hf205a,hf205b"],
            "set_aside": ["hf207a,hf207b"],
            "encounters": [],
            "encounter_sets": ["hf_black_king", "hf_sebastian_shaw", "standard"] + (["expert"] if expert else []),
            "modular_sets": ["hf_hellfire_conclave"]}


# ============================================================ images : numero du scan -> card_id
IMG = {}
for n in (1, 2, 3):
    IMG["Scenario/Black King/%d.png" % n] = "hf20%d" % n
for n in (4, 5):
    IMG["Scenario/Black King/%da.png" % n] = "hf20%da" % n
    IMG["Scenario/Black King/%db.png" % n] = "hf20%db" % n
IMG["Scenario/Black King/6.png"] = "hf206"
IMG["Scenario/Black King/7a.png"] = "hf207a"
IMG["Scenario/Black King/7b.png"] = "hf207b"
for n in range(8, 28):
    IMG["Scenario/Black King/%d.png" % n] = "hf2%02d" % n
for n in range(1, 9):
    IMG["Modules/Sebastian Shaw/%d.png" % n] = "hf33%d" % n
LANDSCAPE = {"hf204a", "hf204b", "hf205a", "hf205b", "hf206", "hf226", "hf227", "hf338"}


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
        sets[CLE_SET] = {"name": PACK, "scenarios": ["hellfire_black_king"], "heroes": [],
                         "encounters": list(ENSEMBLES), "max_id": "hf338"}
        ecrire(p, sets, 1)

    for cle, (nom, lst) in ENSEMBLES.items():
        ecrire(os.path.join(RACINE, "data", "encounter_sets", cle + ".json"), {"version": "0.5.8", "name": nom, "encounters": lst}, 2)
    ecrire(os.path.join(RACINE, "data", "scenarios", "hellfire_black_king.json"), scenario(False), 2)
    ecrire(os.path.join(RACINE, "data", "scenarios", "hellfire_black_king_expert.json"), scenario(True), 2)

    if "--sans-images" not in sys.argv:
        from PIL import Image
        cible = os.path.join(RACINE, "assets", "pics")
        for rel, cid in IMG.items():
            im = Image.open(os.path.join(ZIP, rel)).convert("RGB")
            taille = (882, 615) if cid in LANDSCAPE else (615, 882)
            assert (im.size[0] > im.size[1]) == (taille[0] > taille[1]), (rel, im.size)
            dst = os.path.join(cible, cid + ".jpg")
            if os.path.islink(dst):
                os.remove(dst)
            im.resize(taille, Image.LANCZOS).save(dst, "JPEG", quality=88)
    print("cartes", len(CARTES), "images", len(IMG))


main()
