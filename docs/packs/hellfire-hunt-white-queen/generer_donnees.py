#!/usr/bin/env python3
"""Genere les donnees du scenario 1 « White Queen » de Hellfire Hunt (Dipsome), prefixe `hf`.

Idempotent : relance = meme resultat. cards.json, sets_info.json et prefixes_fanmade.json sont reecrits en RELECTURE-MODIFICATION
sous flock (un autre agent edite les memes fichiers).
Usage : python3 gen_hf_wq.py <racine_moteur> <dossier_zip_extrait>
"""
import fcntl
import io
import json
import os
import sys

RACINE = sys.argv[1]
ZIP = sys.argv[2]  # .../Hellfire Hunt Campaign
PACK = "hellfire_hunt_white_queen"
AUTEUR = "Dipsome"
CLE_SET = "240. Custom (Hellfire Hunt - White Queen)"

WQ, PF, HC, PD = "White Queen", "Perfection", "Hellfire Conclave", "Psionic Delusion"


def carte(cid, typ, nom, set_name, desc, traits, text, **extra):
    c = {"card_id": cid, "type": typ, "name": nom, "subtitle": "", "desc": desc, "traits": traits,
         "set_name": set_name, "text": text, "custom": AUTEUR}
    c.update(extra)
    return c


CARTES = []
A = CARTES.append

# ============================================================ SET « White Queen » (hf101-hf125)
QUOTE_FLIP = "Flip White Queen <i>(whether that card had the [[Illusion]] trait or not)</i>."
A_TXT = ("[star] <b>Forced Response</b>: After White Queen attacks you, discard the top card of the encounter deck. If that card has "
         "the [[Illusion]] trait, reveal it. " + QUOTE_FLIP)
B_INT = ("<b>Forced Interrupt</b>: When White Queen would take any amount of damage from an attack, discard the top card of the "
         "encounter deck. Reduce damage from that attack by the number of boost icons ([boost]) discarded this way.")
B_FLIP = "[star] <b>Forced Response</b>: After White Queen schemes, flip this card."

A(carte("hf101a", "Villain", "* White Queen", WQ, {"HP": "12*", "ATK": "1*", "SCH": "2", "Stage": "1"}, ["HELLFIRE", "PSIONIC"],
        A_TXT + "\n<i>\"You'll all be guests of the Hellfire Club -- for the rest of your natural lives!\"</i>"))
A(carte("hf101b", "Villain", "* White Queen", WQ, {"HP": "12*", "ATK": "2", "SCH": "1*", "Stage": "1"}, ["DIAMOND", "HELLFIRE"],
        B_FLIP + "\n" + B_INT))
A(carte("hf102a", "Villain", "* White Queen", WQ, {"HP": "15*", "ATK": "2*", "SCH": "2", "Stage": "2"}, ["HELLFIRE", "PSIONIC"],
        A_TXT + "\n<i>\"It's a brave new world, Shaw. And I finally get to be the queen you trained me to be.\"</i>"))
A(carte("hf102b", "Villain", "* White Queen", WQ, {"HP": "15*", "ATK": "3", "SCH": "1*", "Stage": "2", "Steady": "1", "Retaliate": "1"},
        ["DIAMOND", "HELLFIRE"], "Steady. Retaliate 1.\n" + B_FLIP + "\n" + B_INT))
A(carte("hf103a", "Villain", "* White Queen", WQ, {"HP": "19*", "ATK": "2*", "SCH": "3", "Stage": "3", "Steady": "1"},
        ["HELLFIRE", "PSIONIC"], "Incite 1. Steady.\n" + A_TXT +
        "\n<i>\"And you still are. Terrified. Knowing that could have been you. Every day spent fighting this ugly war could be your last.\"</i>"))
A(carte("hf103b", "Villain", "* White Queen", WQ, {"HP": "19*", "ATK": "3", "SCH": "1*", "Stage": "3", "Steady": "1", "Retaliate": "1"},
        ["DIAMOND", "HELLFIRE"], "Steady. Retaliate 1.\n" + B_FLIP + "\n" + B_INT))

A(carte("hf104a", "MainScheme", "Infiltrating the Mansion", WQ, {"Stage": "1"}, [],
        "<b>Contents</b>: White Queen (A1) and White Queen (A2). <i>(White Queen (A2) and White Queen (A3) instead for expert mode.)</i> "
        "White Queen, Perfection and Standard encounter sets. Two modular encounter sets <i>(Hellfire Conclave and Psionic Delusion)</i>.\n"
        "<b>Setup</b>: Remove each minion named White Queen from the game."))
A(carte("hf104b", "MainScheme", "Infiltrating the Mansion", WQ, {"StartingThreat": "0", "TargetThreat": "2*", "EscalationThreat": "1*", "Stage": "1"}, [],
        "<i>Emma Frost and her Hellfire Club are trying to breach the security of the Xavier Mansion.</i>\n"
        "<b>When Completed</b>: Flip White Queen and place 1 acceleration token here.\n"
        "<b>Forced Response</b>: After the round ends, advance to stage 2A."))
A(carte("hf105a", "MainScheme", "Locating Cerebro", WQ, {"Stage": "2"}, [],
        "<i>White Queen is now in the mansion. And she is still locating Cerebro, stop her and her army.</i>\n"
        "<b>When Revealed</b>: The first player searches the encounter deck and discard pile for a copy of the Crystalline Adaptation "
        "attachment and reveals it. <i>(Shuffle.)</i>"))
A(carte("hf105b", "MainScheme", "Locating Cerebro", WQ, {"StartingThreat": "2*", "TargetThreat": "9*", "EscalationThreat": "1*", "Stage": "2"}, [],
        "<i>Time is of the essence as they race to secure the powerful mutant-detection system before the White Queen can seize control of it.</i>\n"
        "<b>When Completed</b>: Flip White Queen."))
A(carte("hf106a", "MainScheme", "Hellfire Ascendant", WQ, {"Stage": "3"}, [],
        "<i>With Cerebro in her possession, Emma Frost now seeks to use its power to identify and capture powerful mutants.</i>\n"
        "<b>When Revealed</b>: Search the encounter deck, discard pile, and set-aside area for the Mutant Supremacy side scheme and reveal it. "
        "<i>(Shuffle.)</i>"))
A(carte("hf106b", "MainScheme", "Hellfire Ascendant", WQ, {"StartingThreat": "0", "TargetThreat": "5*", "EscalationThreat": "1*", "Stage": "3"}, [],
        "<i>Having obtained Cerebro, Emma Frost now seeks to use its abilities to conscript the most powerful mutants into the Hellfire Club.</i>\n"
        "<b>If this stage is completed, the players lose the game.</b>"))

A(carte("hf107", "Attachment", "Crystalline Adaptation", WQ, {"ATK+": "1", "SCH+": "1", "Boost": "1", "MaxPerUnit": "1"}, ["SKILL"],
        "Max 1 per enemy.\nAttach to White Queen. Otherwise, this card gains surge.\n"
        "<b>Forced Interrupt</b>: When White Queen is attacked, if she is in [[Psionic]] form, flip her and discard this card.\n<hr />\n"
        "[star] <b>Boost</b>: After this activation, if White Queen is in [[Diamond]] form, flip her and place 2 threat on the main scheme."))
A(carte("hf110", "Attachment", "Psionic Feedback", WQ, {"ATK+": "1", "SCH+": "1"}, ["SKILL"],
        "Attach to White Queen.\n<b>Forced Response</b>: After White Queen flips, give her 1 facedown boost card.\n"
        "<b>Hero Action</b>: Spend [mental][physical] resources → discard this card.\n<hr />\n[star] <b>Boost</b>: Reveal this card."))
A(carte("hf111", "Attachment", "Psionic Maelstrom", WQ, {"ATK+": "0*", "Boost": "3", "Uses": "1,illusion"}, ["ILLUSION", "PSIONIC"],
        "Attach to White Queen.\nUses (1 illusion counter).\n"
        "<b>When Revealed</b>: If White Queen is in [[Psionic]] form, place 1 additional illusion counter here.\n"
        "[star] <b>Forced Response</b>: After White Queen attacks you, take X indirect damage, where X is equal to the number of [[Illusion]] "
        "cards in play. Remove 1 illusion counter from here."))
A(carte("hf112", "Minion", "Illusory Sentinel", WQ, {"HP": "3", "ATK": "2*", "SCH": "1", "Boost": "1", "Quickstrike": "1", "Steady": "1"}, ["ILLUSION"],
        "Quickstrike. Steady.\n[star] Illusory Sentinel's attacks gain overkill.\n<hr />\n"
        "[star] <b>Boost</b>: If this activation is an attack, this card gets +2 boost icons ([boost][boost]) for this activation."))
for scan in (14, 15, 16, 17):
    A(carte("hf1%d" % scan, "Minion", "Phantom Warrior", WQ, {"HP": "2", "ATK": "0", "SCH": "0", "Guard": "1", "Steady": "1", "Toughness": "1"}, ["ILLUSION"],
            "Guard. Steady. Toughness.\n<hr />\n[star] <b>Boost</b>: Put Phantom Warrior into play engaged with you."))
A(carte("hf118", "Treachery", "Fractured Loyalties", WQ, {"Boost": "2"}, ["ILLUSION", "PSIONIC"],
        "<b>When Revealed</b>: Choose an ally you control. It makes a basic attack against you <i>(with exhausting and taking the consequential "
        "damage)</i>. If no attack was made this way, this card gains surge.\n<i>\"They will always hate us.\"</i> —White Queen"))
A(carte("hf120", "Treachery", "Psionic Active", WQ, {"Boost": "3"}, ["SKILL"],
        "<b>When Revealed</b>: If White Queen is in [[Diamond]] form, she attacks you. If you are in alter-ego form, you may choose to exhaust "
        "your identity and take 1 damage to cancel this attack. If White Queen is in [[Psionic]] form, she schemes."))
A(carte("hf122", "Treachery", "Psionic Fortification", WQ, {"Boost": "1"}, ["SKILL"],
        "<b>When Revealed</b>: If White Queen is in [[Diamond]] form, heal 1 damage from her and give her a tough status card. If she is in "
        "[[Psionic]] form, heal 3 damage from her and remove each stunned and confused status card from her.\n<hr />\n"
        "[star] <b>Boost</b>: Give White Queen a tough status card."))
A(carte("hf124", "SideScheme", "Mutant Supremacy", WQ, {"StartingThreat": "2*"}, [],
        "<i>White Queen is primed for battle or her task, driven by her creed.</i>\n"
        "<b>Forced Response</b>: After White Queen attacks and damages a character, stun that character.\n"
        "<b>Forced Response</b>: After White Queen schemes against you, you are confused.\n<hr />\n"
        "[star] <b>Boost</b>: If White Queen is in [[Diamond]] form, you are stunned."))
A(carte("hf125", "SideScheme", "Telepathic Interrogation", WQ, {"StartingThreat": "2", "Crisis": "1", "Boost": "1"}, [],
        "<i>White Queen now controls Xavier Institute students and staff, keeping them from revealing Cerebro's location.</i>\n"
        "<b>When Revealed</b>: Place 2 additional threat here for each [[Illusion]] card in play.\n<hr />\n"
        "[star] <b>Boost</b>: If the White Queen is in [[Psionic]] form, you are confused."))

# ============================================================ MODULE « Perfection » (hf301-hf308)
WQ_ENTER = ("<b>Forced Interrupt</b>: When a White Queen minion attempts to enter play, give the engaged player a facedown encounter card and "
            "discard this card.")
A(carte("hf301", "Minion", "* White Queen", PF, {"HP": "8", "ATK": "2*", "SCH": "1", "Boost": "3", "Toughness": "1"}, ["DIAMOND", "ELITE", "HELLFIRE"],
        "Toughness.\n[star] <b>Forced Response</b>: After White Queen attacks and damages a character, stun that character.\n" + WQ_ENTER))
A(carte("hf302", "Minion", "* White Queen", PF, {"HP": "4", "ATK": "1", "SCH": "2", "Boost": "2", "Guard": "1", "Patrol": "1"}, ["ELITE", "HELLFIRE", "PSIONIC"],
        "Guard. Patrol.\n<b>When Revealed</b>: Reveal the topmost [[Illusion]] attachment in the encounter discard pile.\n" + WQ_ENTER))
CTR = "If the villain or a minion engaged with you has the [[Psionic]] trait, place 1 additional illusion counter here."
A(carte("hf303", "Attachment", "Astral Trap", PF, {"Boost": "2", "Uses": "1,illusion"}, ["ILLUSION", "PSIONIC"],
        "Attach to your identity.\nUses (1 illusion counter).\nAttached character cannot be healed.\n<b>When Revealed</b>: " + CTR +
        "\n<b>Alter-Ego Action</b>: Exhaust a character you control → remove 1 illusion counter from here."))
A(carte("hf304", "Attachment", "Illusory Defender", PF, {"Boost": "3", "Uses": "1,illusion"}, ["ILLUSION", "PSIONIC"],
        "Attach to your identity.\nUses (1 illusion counter).\nAttacks against you cannot be defended by allies or other identities.\n"
        "<b>When Revealed</b>: " + CTR + "\n<b>Forced Response</b>: After the villain attacks you, remove 1 illusion counter from here."))
A(carte("hf305", "Attachment", "Psychic Mirage", PF, {"Boost": "1", "Uses": "1,illusion"}, ["ILLUSION", "PSIONIC"],
        "Attach to your identity.\nUses (1 illusion counter).\nYou cannot change form or ready your identity.\n<b>When Revealed</b>: " + CTR +
        "\n<b>Action</b>: Discard an identity-specific card from your hand → remove 1 illusion counter from here."))
A(carte("hf306", "Attachment", "Psionic Projection", PF, {"Boost": "2", "Uses": "1,illusion"}, ["ILLUSION", "PSIONIC"],
        "Attach to your identity.\nUses (1 illusion counter).\nAs an additional cost for your hero to use a basic power, spend a [mental] resource.\n"
        "<b>When Revealed</b>: " + CTR + "\n<b>Forced Response</b>: After your hero makes a basic attack or a basic thwart, remove 1 illusion "
        "counter from here."))
A(carte("hf307", "Attachment", "Illusion Unraveled", PF, {"Boost": "2"}, ["SKILL"],
        "Attach to the villain.\n<b>Forced Interrupt</b>: When an [[Illusion]] attachment is discarded, give that card to the villain as a "
        "facedown boost card. Discard this card."))
A(carte("hf308", "Treachery", "Illusion Loop", PF, {"Boost": "2"}, ["SKILL"],
        "<b>When Revealed</b>: For each [[Illusion]] attachment in play, if it has any illusion counters on it, place 1 illusion counter on it. "
        "The villain schemes.\n<hr />\n[star] <b>Boost</b>: If there is at least one [[Illusion]] attachment attached to your identity, you are confused."))

# ============================================================ MODULE « Hellfire Conclave » (hf311-hf318)
A(carte("hf311", "Minion", "* Black Bishop", HC, {"HP": "7", "ATK": "1*", "SCH": "1", "Boost": "2", "Toughness": "1", "Villainous": "1"}, ["ELITE", "HELLFIRE"],
        "Toughness. Villainous.\n[star] <b>Forced Response</b>: After Black Bishop attacks and damages a character, confuse that character.\n<hr />\n"
        "[star] <b>Boost</b>: You are confused."))
A(carte("hf312", "Minion", "* White Bishop", HC, {"HP": "6", "ATK": "0*", "SCH": "1", "Boost": "1", "Quickstrike": "1", "Villainous": "1"}, ["ELITE", "HELLFIRE"],
        "Quickstrike. Villainous.\n[star] <b>Forced Response</b>: After White Bishop attacks and damages a character, stun that character.\n<hr />\n"
        "[star] <b>Boost</b>: You are stunned."))
A(carte("hf313", "Minion", "Hellfire Pawn", HC, {"HP": "3", "ATK": "2", "SCH": "1", "Guard": "1", "Patrol": "1", "Surge": "1"}, ["HELLFIRE"],
        "Guard. Patrol. Surge.\n<hr />\n[star] <b>Boost</b>: Put Hellfire Pawn into play engaged with you."))
A(carte("hf317", "SideScheme", "The Hellfire Conclave", HC, {"StartingThreat": "9"}, [],
        "<i>The inner circle is trying to implement their perfect evil plan in secret meeting.</i>\n"
        "Each player engaged with a [[Hellfire]] minion cannot thwart this scheme.\nEach [[Hellfire]] minion gains incite 1.\n"
        "<b>When Revealed</b>: Move 1 threat from here to the main scheme for each [[Elite]], [[Hellfire]] minion in play."))
A(carte("hf318", "SideScheme", "Hellfire Hunt", HC, {"StartingThreat": "2*", "Acceleration": "1", "Boost": "1"}, [],
        "Each [[Hellfire]] minion gets +1 ATK.\n<b>When Revealed</b>: Each player searches the encounter deck and discard pile for a [[Hellfire]] "
        "minion and puts it into play engaged with them."))

# ============================================================ MODULE « Psionic Delusion » (hf321-hf325)
A(carte("hf321", "Attachment", "Echoes of Enmity", PD, {"ATK+": "1", "SCH+": "1", "Boost": "2"}, ["ILLUSION", "PSIONIC"],
        "<b>When Revealed</b>: Search the encounter deck, discard pile, and set-aside area for your nemesis minion, then reveal that minion. "
        "Attach Echoes of Enmity to it. <i>(Shuffle.)</i>\n<hr />\n[star] <b>Boost</b>: Exhaust your identity."))
A(carte("hf322", "Attachment", "Incite Fear", PD, {"Boost": "1"}, ["ILLUSION", "PSIONIC"],
        "Attach to your identity.\nYou cannot resolve triggered abilities in your identity's printed text box (except for <b>Forced</b> abilities).\n"
        "<b>Action</b>: Discard 2 cards at random from your hand → discard this card."))
A(carte("hf324", "Attachment", "Mind Manipulation", PD, {"Boost": "2"}, ["ILLUSION", "PSIONIC"],
        "Treat attached ally as a minion with a blank text box (except for [[TRAITS]]). Attach minion's SCH is equal to its printed THW and it "
        "does not take consequential damage.\n<b>When Revealed</b>: Attach to the ally you control with the lowest cost. If you cannot, this "
        "card gains surge."))
A(carte("hf325", "Attachment", "Veil of Mind's Mirage", PD, {"Boost": "2"}, ["ILLUSION", "PSIONIC"],
        "Attach to your identity.\n<b>When Revealed</b>: Find your nemesis side scheme, then reveal it. If your nemesis side scheme has the "
        "permanent keyword, discard this card.\n<b>Forced Response</b>: After the player phase ends, if your nemesis side scheme is in play, "
        "deal 1 damage to your identity. Otherwise, discard this card."))

# ============================================================ ensembles de rencontre et scenario
ENS_WQ = ["hf107"] * 3 + ["hf110", "hf111", "hf112", "hf112", "hf114", "hf115", "hf116", "hf117", "hf118", "hf118", "hf120", "hf120",
                          "hf122", "hf122", "hf124", "hf125"]
ENS_PF = ["hf301", "hf302", "hf303", "hf304", "hf305", "hf306", "hf307", "hf308"]
ENS_HC = ["hf311", "hf312"] + ["hf313"] * 4 + ["hf317", "hf318"]
ENS_PD = ["hf321", "hf322", "hf322", "hf324", "hf325"]
ENSEMBLES = {"hf_white_queen": ("White Queen", ENS_WQ), "hf_perfection": ("Perfection", ENS_PF),
             "hf_hellfire_conclave": ("Hellfire Conclave", ENS_HC), "hf_psionic_delusion": ("Psionic Delusion", ENS_PD)}


def scenario(expert):
    return {"version": "0.5.8", "name": "White Queen",
            "villain": (["hf102a,hf102b", "hf103a,hf103b"] if expert else ["hf101a,hf101b", "hf102a,hf102b"]),
            "expert": expert,
            "schemes": ["hf104a,hf104b", "hf105a,hf105b", "hf106a,hf106b"],
            "set_aside": [],
            "encounters": [],
            "encounter_sets": ["hf_white_queen", "hf_perfection", "standard"] + (["expert"] if expert else []),
            "modular_sets": ["hf_hellfire_conclave", "hf_psionic_delusion"]}


# ============================================================ images : numero du scan -> card_id
IMG = {}
for n in range(1, 4):
    IMG["Scenario/White Queen/%da.png" % n] = "hf10%da" % n
    IMG["Scenario/White Queen/%db.png" % n] = "hf10%db" % n
for n in (4, 5, 6):
    IMG["Scenario/White Queen/%da.png" % n] = "hf10%da" % n
    IMG["Scenario/White Queen/%db.png" % n] = "hf10%db" % n
for n in (7, 10, 11, 12, 14, 15, 16, 17, 18, 20, 22, 24, 25):
    IMG["Scenario/White Queen/%d.png" % n] = "hf1%02d" % n if n < 10 else "hf1%d" % n
for n in range(1, 9):
    IMG["Modules/Perfection/%d.png" % n] = "hf30%d" % n
for n, cid in {1: "hf311", 2: "hf312", 3: "hf313", 7: "hf317", 8: "hf318"}.items():
    IMG["Modules/hellfire conclave/%d.png" % n] = cid
for n, cid in {1: "hf321", 2: "hf322", 4: "hf324", 5: "hf325"}.items():
    IMG["Modules/Psionic Delusion/%d.png" % n] = cid
LANDSCAPE = {"hf104a", "hf104b", "hf105a", "hf105b", "hf106a", "hf106b", "hf124", "hf125", "hf317", "hf318"}


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
        sets[CLE_SET] = {"name": PACK, "scenarios": ["hellfire_white_queen"], "heroes": [],
                         "encounters": list(ENSEMBLES), "max_id": CARTES[-1]["card_id"]}
        ecrire(p, sets, 1)

        p = os.path.join(RACINE, "tools", "prefixes_fanmade.json")
        reg = lire(p)
        if "hf" not in reg["prefixes"]:
            reg["prefixes"]["hf"] = {"pack": PACK, "libelle": CLE_SET, "cartes": len(CARTES), "depuis": "2026-10-26",
                                     "note": "Cree le 26/10/2026. Auteur Dipsome, campagne Hellfire Hunt (zip Hellfire Hunt Campaign). "
                                             "hf001-hf099 : fondations de campagne (autre agent) ; hf101-hf125 : scenario 1 White Queen ; "
                                             "hf301-hf325 : modules Perfection (301-308), Hellfire Conclave (311-318), Psionic Delusion (321-325). "
                                             "card_id = hf + 100 + numero du scan pour le scenario ; 300/310/320 + numero du scan pour les modules."}
            ecrire(p, reg, 1)

    for cle, (nom, lst) in ENSEMBLES.items():
        ecrire(os.path.join(RACINE, "data", "encounter_sets", cle + ".json"), {"version": "0.5.8", "name": nom, "encounters": lst}, 2)
    ecrire(os.path.join(RACINE, "data", "scenarios", "hellfire_white_queen.json"), scenario(False), 2)
    ecrire(os.path.join(RACINE, "data", "scenarios", "hellfire_white_queen_expert.json"), scenario(True), 2)

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
        im.resize(taille, Image.LANCZOS).save(dst, "JPEG", quality=90)
    print("cartes", len(CARTES), "images", len(IMG))


main()
