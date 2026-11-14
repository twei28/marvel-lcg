#!/usr/bin/env python3
"""Genere les donnees du scenario 5 « Cassandra Nova » de Hellfire Hunt (Dipsome), prefixe `hf`, pack `hellfire_hunt_cassandra_nova`, set 245.

Contenu : scenario (hf601-hf621 = 600 + numero du scan), module Mind Control (hf371-hf376 = 370 + numero du scan) et module Mutant Extinction
Agenda (hf381-hf388 = 380 + numero du scan). Le module Immensity (hf351-hf358) est porte par l'agent de Torn (set 244) : le scenario le
reference par le nom d'ensemble `hf_immensity`.

Idempotent : relance = meme resultat. cards.json, sets_info.json et prefixes_fanmade.json sont reecrits en RELECTURE-MODIFICATION sous flock
(`/tmp/cards_json.lock`) : seules NOS cles sont ecrites (un autre agent edite les memes fichiers).
Usage : python3 generer_donnees.py <racine_moteur> <dossier « Hellfire Hunt Campaign » extrait>
"""
import fcntl
import io
import json
import os
import sys

RACINE = sys.argv[1]
ZIP = sys.argv[2]
PACK = "hellfire_hunt_cassandra_nova"
AUTEUR = "Dipsome"
CLE_SET = "245. Custom (Hellfire Hunt - Cassandra Nova)"

CN, MC, ME = "Cassandra Nova", "Mind Control", "Mutant Extinction Agenda"


def carte(cid, typ, nom, set_name, desc, traits, text, **extra):
    c = {"card_id": cid, "type": typ, "name": nom, "subtitle": "", "desc": desc, "traits": traits,
         "set_name": set_name, "text": text, "custom": AUTEUR}
    c.update(extra)
    return c


CARTES = []
A = CARTES.append

# ============================================================ SCENARIO « Cassandra Nova » (hf601-hf621)
FR_A = ("[star] <b>Forced Response</b>: After Cassandra Nova activates against you, place 1 Cassandra Controls counter on your identity card.")
A(carte("hf601", "Villain", "* Cassandra Nova", CN, {"HP": "15*", "ATK": "1*", "SCH": "2*", "Stage": "1"}, ["MUMMUDRAI", "PSIONIC"],
        FR_A + "\n<i>\"People must learn to hate. I'm going to be their teacher.\"</i>"))
A(carte("hf602", "Villain", "* Cassandra Nova", CN, {"HP": "18*", "ATK": "2*", "SCH": "3*", "Stage": "2", "Steady": "1"}, ["MUMMUDRAI", "PSIONIC"],
        "Steady.\n<b>When Revealed</b>: Place 1 Cassandra Controls counter on each identity.\n" + FR_A +
        "\n<i>\"How can it be murder when they're germs or vermin?\"</i>"))
A(carte("hf603", "Villain", "* Cassandra Nova", CN, {"HP": "20*", "ATK": "3*", "SCH": "3*", "Stage": "3", "Stalwart": "1"}, ["MUMMUDRAI", "PSIONIC"],
        "Stalwart.\n<b>When Revealed</b>: Place 1 Cassandra Controls counter on each identity and place 1[per_hero] acceleration tokens on the main "
        "scheme.\n" + FR_A +
        "\n<i>\"From here I can reach out, take hold of every remaining mutant mind on Earth and extinguish it. But I only need one.\"</i>"))

A(carte("hf604a", "MainScheme", "Diplomatic Sabotage", CN, {"Stage": "1"}, [],
        "<b>Contents</b>: Cassandra Nova (I) and Cassandra Nova (II). <i>(Cassandra Nova (II) and Cassandra Nova (III) instead for expert mode.)</i> "
        "Cassandra Nova, Immensity and Standard encounter sets. Two modular encounter sets <i>(Mind Control and Mutant Extinction Agenda)</i>.\n"
        "<b>Setup</b>: Remove Cassandra Nova minion from the game. Put the Cassandra Domination environment into play. In expert mode, advance to "
        "stage 2A."))
A(carte("hf604b", "MainScheme", "Diplomatic Sabotage", CN, {"StartingThreat": "1*", "TargetThreat": "7*", "EscalationThreat": "1*", "Stage": "1"}, [],
        "<b>Forced Response</b>: After your turn ends, if there is Cassandra Controls counter on your identity, you must choose to either place "
        "1 threat here or take 2 damage.\n<b>Hero Action</b>: Discard 5 cards from the top of the encounter deck → remove a Cassandra Controls "
        "counter from your identity. <i>(Limit once per round per player.)</i>"))
A(carte("hf605a", "MainScheme", "Silent Takeover", CN, {"Stage": "2"}, [],
        "<i>Cassandra prepares to have a war with the mutants and turn the heroes' enemies into her personal army.</i>\n"
        "<b>When Revealed</b>: Each player finds their own nemesis minion and put it into play engaged with themself."))
A(carte("hf605b", "MainScheme", "Silent Takeover", CN, {"StartingThreat": "2*", "TargetThreat": "11*", "EscalationThreat": "1*", "Stage": "2"}, [],
        "<b>Forced Response</b>: After your turn ends, if there is Cassandra Controls counter on your identity, you must choose to either place "
        "2 threat here or deal yourself 1 facedown encounter card.\n<b>Hero Action</b>: Discard 6 cards from the top of the encounter deck "
        "→ remove a Cassandra Controls counter from your identity. <i>(Limit once per round per player.)</i>"))
A(carte("hf606a", "MainScheme", "Mutant Extermination", CN, {"Stage": "3"}, [],
        "<i>Nova furthered her goal with the creation of Sentinites, allowed them to detect mutants in their vicinity and sent them into a "
        "murderous rage.</i>\n<b>When Revealed</b>: Deal each player 1 facedown encounter card for each character they control."))
A(carte("hf606b", "MainScheme", "Mutant Extermination", CN, {"StartingThreat": "3*", "TargetThreat": "13*", "EscalationThreat": "1*", "Stage": "3"}, [],
        "<b>Forced Response</b>: After your turn ends, if there is Cassandra Controls counter on your identity, you must choose to either place "
        "3 threat here or discard 1 card from your hand.\n<b>Hero Action</b>: Discard 7 cards from the top of the encounter deck → remove a "
        "Cassandra Controls counter from your identity. <i>(Limit once per round per player.)</i>\n"
        "<b>When this scheme is completed, the players lose the game.</b>"))

A(carte("hf607", "Environment", "Cassandra Domination", CN, {}, [],
        "<b>Forced Response</b>: After a Cassandra Controls counter is placed on your identity card, if there is at least 3 Cassandra Controls "
        "counter, remove 3 Cassandra Controls counter from it → you choose one: place 2 threat on each scheme, stun and confuse your "
        "identity, or deal 3 indirect damage to another friendly character."))

OBL_EXPLODING = ("Each encounter card you revealed gains peril.\n<b>Forced Response</b>: After your turn ends, discard cards you control that the "
                 "total resource cost of cards is at least 2. Take 1 damage for each card you discarded. Then, discard this card. Otherwise, deal "
                 "yourself 1 facedown encounter card.")
for n in (8, 9):
    A(carte("hf6%02d" % n, "Obligation", "Exploding Their Head", CN, {"GiveTo": ""}, [], OBL_EXPLODING))
OBL_PC = ("<b>Forced Response</b>: After your turn ends, Cassandra Nova schemes. Confuse your identity, then, discard this card.\n"
          "<b>Alter-Ego Action</b>: Exhaust your identity → discard this card.")
for n in (10, 11, 12):
    A(carte("hf6%02d" % n, "Obligation", "Psychic Control", CN, {"Boost": "3", "GiveTo": ""}, [], OBL_PC))
SYM = ("<b>When Revealed</b>: Discard X cards from the encounter deck, where X is equal to double the villain's stage number. Each time a "
       "Cassandra Nova card is discarded this way, place 1 Cassandra Controls counter on your identity.")
for n in (13, 14, 15):
    A(carte("hf6%02d" % n, "Treachery", "Shatter Your Mind", CN, {"Boost": "2"}, ["PSIONIC", "TACTIC"], SYM))
COMBO = ("<b>When Revealed</b>: Cassandra Nova activates against you. You are stunned.\n<hr />\n[star] <b>Boost</b>: If this activation is an attack, "
         "this attack gains overkill and piercing. Otherwise, place threat on the main scheme equals to the number of Cassandra Controls counter "
         "on your identity.")
for n in (16, 17):
    A(carte("hf6%02d" % n, "Treachery", "Psychic Combo", CN, {"Boost": "1"}, ["PSIONIC", "TACTIC"], COMBO))
LEECH = ("<b>When Revealed</b>: Discard your hand. Draw up to your hand size. For each card you discard in this way, heal 1 damage from Cassandra "
         "Nova, if you cannot, place a Cassandra Controls counter on your identity.")
for n in (18, 19):
    A(carte("hf6%02d" % n, "Treachery", "Psychic Leech", CN, {"Boost": "1"}, ["PSIONIC", "TACTIC"], LEECH))
A(carte("hf620", "SideScheme", "Global Opinion Controls", CN, {"StartingThreat": "2"}, [],
        "Treat each support's text box as if it were blank.\n<b>When Revealed</b>: For each Cassandra Controls counter in play, place 1 threat "
        "here.\n<hr />\n[star] <b>Boost</b>: Place 2 Cassandra Controls counters on your identity card."))
A(carte("hf621", "SideScheme", "The Hate Machine", CN, {"StartingThreat": "2"}, [],
        "While at least 1 Cassandra Control counter on your identity, you cannot attack Cassandra Nova or thwart the main scheme.\n"
        "<b>When Revealed</b>: For each Cassandra Controls counter in play, place 1 threat here.\n<hr />\n[star] <b>Boost</b>: Reveal this card."))

# ============================================================ MODULE « Mind Control » (hf371-hf376)
SPEND_MM = "[mental][mental]"
A(carte("hf371", "Attachment", "Psychic Aegis", MC, {"Setup": "1"}, ["PSIONIC"],
        "Setup. Attach to the villain.\nAttached character cannot be confused.\nAttached character cannot take damage from a player while that "
        "player is confused.\n<b>Action</b>: Spend %s resources → discard this card.\n<hr />\n[star] <b>Boost</b>: Reveal this card." % SPEND_MM))
A(carte("hf372", "Attachment", "False Reality", MC, {"Boost": "1"}, ["ILLUSION", "PSIONIC"],
        "Attach to the main scheme.\n<b>Forced Interrupt</b>: When a player would remove threat from the main scheme, prevent 2 of that threat "
        "from being removed. Then, confuse that player. <i>(Limit once per phase.)</i>\n<b>Hero Action</b>: Spend %s resource → discard "
        "this card." % SPEND_MM))
A(carte("hf373", "Attachment", "Mind Maze", MC, {"Boost": "1"}, ["ILLUSION", "PSIONIC"],
        "Attach to your identity.\n<b>Forced Interrupt</b>: When you would thwart, discard this card instead. Then, you are confused.\n"
        "<b>Action</b>: Spend %s resources → discard this card." % SPEND_MM))
for n in (4, 5):
    A(carte("hf37%d" % n, "Treachery", "Illusory Attacks", MC, {"Boost": "1"}, ["ILLUSION", "PSIONIC"],
            "<b>When Revealed</b>: You are confused. Deal 1 damage to each confused character in play.\n<hr />\n[star] <b>Boost</b>: You are confused."))
A(carte("hf376", "Treachery", "Mind Shatter", MC, {"Boost": "1", "Peril": "1"}, ["ILLUSION", "PSIONIC"],
        "Peril.\n<b>When Revealed</b>: You are confused. You may discard any number of cards from your hand. Then, deal X damage to each "
        "identity in play, where X is equal to half of the number of cards from your hand."))

# ============================================================ MODULE « Mutant Extinction Agenda » (hf381-hf388)
A(carte("hf381", "SideScheme", "* Mutant Extinction Agenda", ME, {"StartingThreat": "2*", "Victory": "1", "Boost": "1"}, [],
        "Victory 1.\nEach [[Sentinel]] minion gets +1 ATK and +1 SCH. This card cannot be defeated while a [[Sentinel]] minion is in play.\n"
        "<b>When Revealed</b>: Each player search the encounter deck and discard pile for a [[Sentinel]] minion in player order. Put it into "
        "play engaged with you.\n<hr />\n[star] <b>Boost</b>: Put this card into play."))
for n in (2, 3, 4, 5):
    A(carte("hf38%d" % n, "Minion", "Wild Sentinel", ME, {"HP": "4", "ATK": "2", "SCH": "1", "Boost": "3"}, ["SENTINEL"],
            "<b>When Defeated</b>: The defeating player chooses to either take 2 damage or place this card on the bottom of the encounter deck "
            "instead of the discard pile."))
for n in (6, 7):
    A(carte("hf38%d" % n, "Treachery", "E for Extinction", ME, {"Boost": "1"}, ["ATTACK"],
            "<b>When Revealed</b>: For each [[Sentinel]] minion in play, deal 1 indirect damage to each player. If there is no [[Sentinel]] minion "
            "in play, search the encounter deck and discard pile for a [[Sentinel]] minion and put it into play engaged with you."))
A(carte("hf388", "SideScheme", "* Worldwide Sentinel Deployment", ME, {"StartingThreat": "3*", "Victory": "1", "Hazard": "1", "Boost": "2"}, [],
        "Victory 1.\n<b>When Revealed</b>: Each player search the encounter deck and discard pile for a [[Sentinel]] minion in player order. "
        "Put it into play engaged with you."))

# ============================================================ ensembles de rencontre et scenarios
ENS_CN = ["hf608", "hf609", "hf610", "hf611", "hf612", "hf613", "hf614", "hf615", "hf616", "hf617", "hf618", "hf619", "hf620", "hf621"]
ENS_MC = ["hf371", "hf372", "hf373", "hf374", "hf375", "hf376"]
ENS_ME = ["hf381", "hf382", "hf383", "hf384", "hf385", "hf386", "hf387", "hf388"]
ENSEMBLES = {"hf_cassandra_nova": ("Cassandra Nova", ENS_CN), "hf_mind_control": ("Mind Control", ENS_MC),
             "hf_mutant_extinction_agenda": ("Mutant Extinction Agenda", ENS_ME)}


def scenario(expert):
    return {"version": "0.5.8", "name": "Cassandra Nova",
            "villain": (["hf602", "hf603"] if expert else ["hf601", "hf602"]),
            "expert": expert,
            "schemes": ["hf604a,hf604b", "hf605a,hf605b", "hf606a,hf606b"],
            "set_aside": ["hf607"],
            "encounters": [],
            "encounter_sets": ["hf_cassandra_nova", "hf_immensity", "standard"] + (["expert"] if expert else []),
            "modular_sets": ["hf_mind_control", "hf_mutant_extinction_agenda"]}


# ============================================================ images : numero du scan -> card_id
IMG = {}
for n in (1, 2, 3) + tuple(range(7, 22)):
    IMG["Scenario/Cassandra Nova/%d.png" % n] = "hf6%02d" % n
for n in (4, 5, 6):
    for f in "ab":
        IMG["Scenario/Cassandra Nova/%d%s.png" % (n, f.upper())] = "hf60%d%s" % (n, f)
for n in range(1, 7):
    IMG["Modules/Mind Control/%d.png" % n] = "hf37%d" % n
for n in range(1, 9):
    IMG["Modules/Mutant Extinction Agenda/%d.png" % n] = "hf38%d" % n
LANDSCAPE = {"hf604a", "hf604b", "hf605a", "hf605b", "hf606a", "hf606b", "hf620", "hf621", "hf381", "hf388"}


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


NOTE_PREFIXE = (" Scenario 5 Cassandra Nova (pack hellfire_hunt_cassandra_nova, set 245) : hf601-hf621 (600 + numero du scan) ; modules Mind Control "
                "hf371-hf376 et Mutant Extinction Agenda hf381-hf388 (370 / 380 + numero du scan).")


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
        sets[CLE_SET] = {"name": PACK, "scenarios": ["hellfire_cassandra_nova"], "heroes": [], "encounters": list(ENSEMBLES), "max_id": "hf621"}
        ecrire(p, sets, 1)

        p = os.path.join(RACINE, "tools", "prefixes_fanmade.json")
        reg = lire(p)
        if "hf" in reg["prefixes"] and NOTE_PREFIXE not in reg["prefixes"]["hf"].get("note", ""):
            reg["prefixes"]["hf"]["note"] = reg["prefixes"]["hf"].get("note", "") + NOTE_PREFIXE
            ecrire(p, reg, 1)

    for cle, (nom, lst) in ENSEMBLES.items():
        ecrire(os.path.join(RACINE, "data", "encounter_sets", cle + ".json"), {"version": "0.5.8", "name": nom, "encounters": lst}, 2)
    ecrire(os.path.join(RACINE, "data", "scenarios", "hellfire_cassandra_nova.json"), scenario(False), 2)
    ecrire(os.path.join(RACINE, "data", "scenarios", "hellfire_cassandra_nova_expert.json"), scenario(True), 2)

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
        im.resize(taille, Image.LANCZOS).save(dst, "JPEG", quality=88, optimize=True)
    print("cartes", len(CARTES), "images", len(IMG))


main()
