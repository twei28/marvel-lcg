# -*- coding: utf-8 -*-
"""Importe les 50 cartes d'aspect / Basic « Starjammers » (Phenexian et Mysteltainn, prefixe `sy`, pack `starjammers_aspects`).

Source : zip `Starjammers-20261025T195726Z-1-001.zip`, dossier `Aspect and Basic Cards/` (50 PNG).
Numerotation : le numero imprime en pied de carte (77 a 126) moins 76 : 77 -> sy001 ... 126 -> sy050. Lilandra n'a PAS de numero
imprime : 111 par deduction (seul trou de la suite). Transcription carte par carte : docs/packs/starjammers-aspects/TRANSCRIPTIONS.md.

Ce script ECRIT la liste `starjammers_aspects` de `data/cards.json` (idempotent : il remplace la liste du pack, il ne touche rien
d'autre). Les autres agents editent le meme fichier : le script prend `flock /tmp/cards_json.lock` pendant la lecture-ecriture.
Le checksum du fichier se recalcule APRES (tools/recalculer_checksums.py).

Usage : python3 tools/importer_cartes_starjammers_aspects.py [--ecrire]
        (sans --ecrire : verifie la table et affiche ce qui serait ecrit)
"""
import fcntl
import io
import json
import os
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARTES = os.path.join(RACINE, "data", "cards.json")
PACK = "starjammers_aspects"
SET = "Starjammers Aspects"
AUTEUR = "Phenexian and Mysteltainn"
VERROU = "/tmp/cards_json.lock"


def _a(cid, nom, sous_titre, cout, pv, atq, ctr, res, classe, traits, texte):
    """Un allie."""
    return {"card_id": cid, "type": "Ally", "name": nom, "subtitle": sous_titre,
            "desc": {"Cost": cout, "HP": pv, "ATK": atq, "THW": ctr, "RES": res, "Class": classe},
            "traits": traits, "set_name": SET, "text": texte, "custom": AUTEUR}


def _c(cid, type_, nom, desc, traits, texte):
    """Tout le reste (evenement, amelioration, soutien, manigance joueur)."""
    return {"card_id": cid, "type": type_, "name": nom, "subtitle": "", "desc": desc,
            "traits": traits, "set_name": SET, "text": texte, "custom": AUTEUR}


REQ = "Requirement ([energy][mental][physical])."
ICONES = "([star] and [boost])"

CARTES_SY = [
    # ----------------------------------------------------------------------------------------------------- Basic (77-91)
    _a("sy001", "* Ch'od", "", "4", "5", "3**", "2**", "R", "Basic", ["STARJAMMER"],
       "<b>Response</b>: After Ch'od enters play, search your deck and discard pile for a [[VEHICLE]] or [[TECH]] card and add it to your hand.\n"
       "<i>\"I will not have someone going nutso when they are elbow-deep in the nervous system of my ship!\"</i>"),
    _a("sy002", "* Corsair", "Christopher Summers", "4", "3", "2*", "2*", "Y", "Basic", ["STARJAMMER"],
       "<b>Interrupt</b>: After you play Corsair from your hand, tuck each card you used to pay for him under here.\n"
       "[star] <b>Response</b>: After you attack or thwart with Corsair, add a card tucked under him to your hand."),
    _a("sy003", "* Hepzibah", "", "3", "3", "1*", "1*", "Y", "Basic", ["STARJAMMER"],
       "<b>Interrupt</b>: When Hepzibah attacks an enemy, exhaust a [[WEAPON]] you control → Hepzibah gets +2 ATK for that attack. "
       "That attack gains overkill.\n<i>\"Killer instinct, Hepzibah lacks not\"</i>"),
    _a("sy004", "* Sikorsky", "", "2", "2", "1*", "1*", "B", "Basic", ["AERIAL", "PSIONIC", "STARJAMMER"],
       "<b>Response</b>: After Sikorsky enters play, heal 1 damage from a character.\n"
       "<i>\"Physician, I am. Best for patient, I know what. Asking am not. Telling!\"</i>"),
    _a("sy005", "* Waldo", "", "3", "3", "1*", "2*", "B", "Basic", ["ANDROID", "STARJAMMER"],
       "[star] <b>Response</b>: After Waldo uses a basic power, ready a [[VEHICLE]] you control.\n"
       "<i>\"I copy. How are things dirt side?\"</i>"),
    _a("sy006", "* Raza Longknife", "", "3", "3", "2*", "1*", "R", "Basic", ["CYBORG", "STARJAMMER"],
       "Raza Longknife gets +1 hit point for each upgrade attached to him.\n<i>\"Starjammers don't know how to lose.\"</i>"),
    _c("sy007", "Event", "Life-Bonded Crewmates",
       {"Cost": "1", "RES": "R", "MaxPerDeck": "1", "TeamUp": "Corsair;Hepzibah", "Class": "Basic"}, [],
       "Team-Up (Corsair and Hepzibah). Max 1 per deck.\n"
       "<b>Action</b>: Heal 2 damage from Corsair and Hepzibah. Search your discard for an event and add it to your hand."),
    _c("sy008", "Event", "Steadfast Companions",
       {"Cost": "2", "RES": "B", "MaxPerDeck": "1", "TeamUp": "Ch'od;Raza Longknife", "Class": "Basic"}, [],
       "Team Up (Ch'od and Raza Longknife). Max 1 per deck.\n"
       "<b>Action:</b> Give Ch'od and Raza Longknife each a tough status card. Search your deck for an upgrade and add it to your hand."),
    _c("sy009", "PlayerSideScheme", "* Skillful Execution",
       {"Cost": "0", "RES": "Y", "StartingThreat": "2*", "Victory": "0", "Class": "Basic"}, [],
       "Victory 0.\n<b>When Defeated</b>: Each player may search their deck and discard pile for a [[SKILL]] card and add it to their hand. "
       "Reduce the cost of each [[SKILL]] played this phase by 1.\n<i>\"Okay, here's how we do the deed.\"</i> —Corsair"),
    _c("sy010", "Support", "* Center Section Garden",
       {"Cost": "2", "RES": "B", "Class": "Basic"}, ["LOCATION", "STARJAMMER"],
       "<b>Alter-Ego Response</b>: After you make a basic recovery, exhaust Centre Section Garden → heal 2 damage from your identity "
       "or a [[STARJAMMER]] character.\n<i>\"I just wanted to carry something good with me.\"</i> —Corsair"),
    _c("sy011", "Support", "* Standing Still",
       {"Cost": "3", "RES": "B", "Class": "Basic"}, ["LOCATION", "PLANET"],
       "<b>Resource</b>: Exhaust Standing Still → generate a [wild] resource for a player whose identity has the [[OUTLAW]] or "
       "[[STARJAMMER]] trait.\n<i>An anarchist planet within the independent net of worlds called the clench, and the free base from "
       "which the Starjammers operate.</i>"),
    _c("sy012", "Support", "* The Starjammer",
       {"Cost": "2", "RES": "Y", "Class": "Basic"}, ["STARJAMMER", "VEHICLE"],
       "If each of your allies has the [[STARJAMMER]] trait, increase your ally limit by 1.\n"
       "<b>Hero Interrupt</b>: When a [[STARJAMMER]] character uses a basic power, exhaust The Starjammer → that character gets +1 to "
       "that power for this use."),
    _c("sy013", "Upgrade", "Honorary Starjammer",
       {"Cost": "0", "RES": "Y", "MaxPerUnit": "1", "Class": "Basic"}, ["TITLE"],
       "Play only if your identity has the [[STARJAMMER]] trait.\nAttach to a friendly character. Max 1 per character.\n"
       "Attached character gets +1 hit point and gains the [[STARJAMMER]] trait."),
    _c("sy014", "Upgrade", "Pirate's Rapier",
       {"Cost": "1", "RES": "R", "MaxPerUnit": "1", "Class": "Basic"}, ["WEAPON"],
       "Attach to a [[STARJAMMER]] ally. Max 1 per ally.\nAttached ally gets +1 ATK and its attacks gain piercing.\n"
       "<i>\"Most armor, spacesuits, they're blaster-proof. A good blade can slice one open.\"</i> —Corsair"),
    _c("sy015", "Upgrade", "Stolen Goods",
       {"Cost": "0", "RES": "G", "MaxPerDeck": "2", "Class": "Basic"}, ["ITEM"],
       "Max 2 per deck.\n<b>Resource</b>: Discard this card → generate [wild][wild]. Trigger this ability only if you have the "
       "[[OUTLAW]] trait.\n<i>\"No sense letting all this stuff go to waste...\"</i> —Raza Longknife"),
    # ------------------------------------------------------------------------------------------------ Aggression (92-100)
    _a("sy016", "* Binary", "Carol Danvers", "5", "4", "3*", "2*", "Y", "Aggression", ["AERIAL", "STARJAMMER"],
       "<b>Response</b>: After Binary enters play, discard the top 4 cards of your deck. If you discard a printed [physical] resource, "
       "deal 3 damage to an enemy. If you discard a printed [energy] resource, stun an enemy.\n<i>\"Now I can really cut loose!\"</i>"),
    _a("sy017", "* Korvus Rook'shir", "", "3", "3", "1*", "1*", "R", "Aggression", ["PSIONIC", "SHI'AR", "STARJAMMER"],
       "<b>Response</b>: After Korvus Rook'shir enters play, find Blade of the Phoenix and attach it to him.\n"
       "<i>\"Listen to me. You can't beat this blade.\"</i>"),
    _c("sy018", "Upgrade", "* Blade of the Phoenix",
       {"Cost": "1", "RES": "YB", "Class": "Aggression", "Linked": "Korvus Rook'shir"}, ["ARTIFACT", "WEAPON"],
       "Linked (Korvus Rook'shir)\nAttach to an ally.\nAttached ally gets +2 ATK. If the attached ally doesn't have the [[PSIONIC]] "
       "trait, it takes +1 consequential damage after it attacks."),
    _a("sy019", "* Marvel Girl", "Rachel Summers", "3", "3", "2*", "2**", "B", "Aggression", ["PSIONIC", "STARJAMMER", "X-MEN"],
       "<b>Interrupt</b>: When Marvel Girl attacks, choose one:\n• That attack gains piercing.\n• That attack gains ranged.\n"
       "• That attack gains overkill."),
    _c("sy020", "Event", "Critical Blow",
       {"Cost": "3", "RES": "Y", "Requirement": "YBR", "Class": "Aggression"}, ["ATTACK", "THWART"],
       REQ + "\n<b>Hero Action</b> <i>(attack/thwart)</i>: Deal 4 damage to an enemy. Remove threat from a scheme equal to the damage "
       "dealt this way. This attack gains piercing.\n<i>\"You would be wise to surrender now.\"</i> —Ch'od"),
    _c("sy021", "Event", "Outlaw Justice",
       {"Cost": "2", "RES": "Y", "Class": "Aggression", "Alliance": "1"}, ["ATTACK", "THWART"],
       "Alliance.\n<b>Hero Action</b> <i>(attack/thwart)</i>: Exhaust a [[STARJAMMER]] character and a [[GUARDIAN]] character → deal X "
       "damage among enemies in play and remove X threat from among schemes in play, where X is the combined ATK of the two exhausted "
       "characters."),
    _c("sy022", "Event", "Reckless Attack",
       {"Cost": "1", "RES": "R", "Class": "Aggression"}, ["ATTACK"],
       "<b>Hero Action</b> <i>(attack)</i>: Discard the top card of the encounter deck. Deal 1 damage to your identity for each icon "
       + ICONES + " in that card's boost area → deal 4 damage to an enemy.\n<i>\"This is gonna hurt.\"</i> —Corsair"),
    _c("sy023", "Upgrade", "Energy Cannon",
       {"Cost": "1", "RES": "Y", "Restricted": "1", "Class": "Aggression"}, ["TECH", "WEAPON"],
       "Restricted.\n<b>Action</b>: Exhaust Energy Cannon → place 1 charge counter on it.\n<b>Hero Action</b>: Discard Energy Cannon → "
       "deal X damage divided among enemies as you choose, where X is equal to the number of charge counters on Energy Cannon."),
    _c("sy024", "Upgrade", "Longarm Blaster",
       {"Cost": "2", "RES": "B", "MaxPerUnit": "1", "Class": "Aggression"}, ["TECH", "WEAPON"],
       "Attach to a [[STARJAMMER]] ally. Max 1 per ally.\n<b>Response</b>: After you defend against an attack, exhaust the attached "
       "ally → deal X damage to an enemy, where X is the attached ally's printed attack."),
    # ---------------------------------------------------------------------------------------------------- Justice (101-108)
    _a("sy025", "* Havok", "Alex Summers", "4", "3", "1*", "1*", "B", "Justice", ["STARJAMMER", "X-MEN"],
       "<b>Forced Response</b>: After Havok enters play, tuck the top 3 cards of the encounter deck under him.\n"
       "[star] <b>Forced Interrupt</b>: When Havok uses a basic power, discard a card tucked under him. He gets +1 to that basic power "
       "for each icon " + ICONES + " in that card's boost area."),
    _a("sy026", "* Polaris", "Lorna Dane", "3", "3", "2**", "2*", "Y", "Justice", ["STARJAMMER", "X-MEN"],
       "[star] <b>Response</b>: After Polaris takes consequential damage from thwarting, if that thwart removed the last threat from a "
       "scheme, give a her a tough status card.\n<i>\"We'll hold out as long as it takes. We have to.\"</i>"),
    _c("sy027", "Event", "Freedom Fighters",
       {"Cost": "1", "RES": "R", "Class": "Justice", "Alliance": "1"}, ["THWART"],
       "Alliance.\n<b>Response</b> <i>(thwart)</i>: When the villain activates against a player, exhaust a [[STARJAMMER]] character and "
       "an [[X-MEN]] character → cancel that activation. Remove X threat from a scheme, where X is the combined THW of the two "
       "exhausted characters."),
    _c("sy028", "Event", "Masterstroke",
       {"Cost": "3", "RES": "B", "Requirement": "YBR", "Class": "Justice"}, ["THWART"],
       REQ + "\n<b>Hero Action</b> <i>(thwart)</i>: Discard the top 4 cards of the encounter deck, then for each card discarded this way "
       "choose one:\n• Remove threat from a scheme equal to the number of boost icons ([boost]) on that card.\n• Place that card on top "
       "of the encounter deck and draw 1 card."),
    _c("sy029", "Event", "Reckless Maneuver",
       {"Cost": "1", "RES": "R", "Class": "Justice"}, ["THWART"],
       "<b>Hero Action</b> <i>(thwart)</i>: Discard the top card of the encounter deck. Deal 1 damage to your identity for each icon "
       + ICONES + " in that card's boost area → remove 4 threat from a scheme.\n<i>\"If anyone here has a god, start flattering it.\"</i> —Corsair"),
    _c("sy030", "Support", "* Helek",
       {"Cost": "2", "RES": "B", "Class": "Justice"}, ["KREE", "PERSONA"],
       "Reduce the cost to play Helek by 2 if your identity has the [[STARJAMMER]] trait.\n<b>Response</b>: After a player reveals a "
       "treachery card, exhaust Helek → that player draws a card.\n<i>\"Anarchy is no good without freedom of information.\"</i>"),
    _c("sy031", "Upgrade", "Disruptor Ray",
       {"Cost": "2", "RES": "B", "Restricted": "1", "Uses": "2,charge", "Class": "Justice"}, ["TECH", "WEAPON"],
       "Restricted. Uses (2 charge counters).\n<b>Action</b>: Exhaust disruptor ray and remove 1 charge counter from it → choose an "
       "attachment, non-[[ELITE]] minion, or side scheme. Until the end of the round, treat that card's printed text box as if it were "
       "blank <i>(except for [[TRAITS]])</i>."),
    _c("sy032", "Upgrade", "Tactical Teleporter",
       {"Cost": "1", "RES": "Y", "MaxPerUnit": "1", "Class": "Justice"}, ["TECH"],
       "Attach to a [[STARJAMMER]] ally. Max 1 per ally.\nAttached ally gets +1 THW and ignores the guard keyword, the patrol keyword, "
       "and the crisis icon ([crisis])."),
    # ------------------------------------------------------------------------------------------------ Leadership (109-117)
    _a("sy033", "* Cyclops", "Scott \"Slim\" Summers", "2", "2", "1*", "1*", "R", "Leadership", ["CHAMPION", "STARJAMMER"],
       "[star] <b>Response</b>: After Cyclops uses a basic power, choose another character. That character gets +1 to that basic power "
       "until the end of the phase.\n<i>\"I've seen the man I become. I don't like him very much.\"</i>"),
    _a("sy034", "* Keeyah", "", "3", "3", "1*", "2*", "Y", "Leadership", ["KREE", "STARJAMMER"],
       "[star] <b>Response</b>: After Keeyah uses a basic power, choose another ally → that ally uses the same basic power without "
       "exhausting. <i>(They take consequential damage as normal.)</i>\n<i>\"System drive is ticking over. Ready when you are.\"</i>"),
    _a("sy035", "* Lilandra", "Lilandra Neramani", "3", "3", "1*", "2*", "B", "Leadership", ["PSIONIC", "SHI'AR", "STARJAMMER"],
       "<b>Action</b>: Exhaust Lilandra and deal 1 damage to her → choose another ally. Until the end of the phase the chosen ally does "
       "not take consequential damage.\n<i>\"War is coming, and we can no longer fight it alone.\"</i>"),
    _c("sy036", "Event", "Decisive Action",
       {"Cost": "3", "RES": "Y", "Requirement": "YBR", "Class": "Leadership"}, ["ATTACK", "THWART"],
       REQ + "\n<b>Hero Action</b>: Your hero gets +1 ATK and +1 THW until the end of the phase. Make a basic attack without exhausting. "
       "Make a basic thwart without exhausting."),
    _c("sy037", "Event", "Far-Flung Family",
       {"Cost": "4", "RES": "B", "Class": "Leadership", "Alliance": "1"}, [],
       "Alliance.\n<b>Action</b>: Exhaust a [[STARJAMMER]] character and an [[X-MEN]] character → as a group, the players search their "
       "decks for a total of 1 [[STARJAMMER]] ally and 1 [[X-MEN]] ally and put them into play exhausted."),
    _c("sy038", "Event", "Reckless Charge",
       {"Cost": "2", "RES": "R", "Class": "Leadership"}, ["TACTIC"],
       "<b>Hero Action</b>: Discard the top card of the encounter deck. Deal 1 damage to your identity for each icon " + ICONES
       + " in that card's boost area → ready up to 3 characters.\n<i>\"Their defenses are strong, so we hit them fast.\"</i> —Corsair"),
    _c("sy039", "Support", "Targeting Station",
       {"Cost": "2", "RES": "B", "Uses": "3,ammo", "Class": "Leadership"}, ["LOCATION", "TECH", "WEAPON"],
       "Uses (3 ammo counters).\n<b>Action</b>: Exhaust a character you control and remove 1 ammo counter from this card → deal 3 "
       "damage to an enemy.\n<i>\"Main guns cycled. Secondaries and deliveries standing by.\"</i> —Hepzibah"),
    _c("sy040", "Upgrade", "* Captain of the Starjammer",
       {"Cost": "3", "RES": "Y", "Class": "Leadership"}, ["TITLE"],
       "Your identity gains the [[STARJAMMER]] trait.\n<b>Hero Response</b>: After you use a basic power, each [[STARJAMMER]] ally you "
       "control gets +1 to that basic power until the end of the phase."),
    _c("sy041", "Upgrade", "Jet Bike",
       {"Cost": "1", "RES": "Y", "MaxPerUnit": "1", "Class": "Leadership"}, ["VEHICLE"],
       "Attach to a [[STARJAMMER]] ally. Max 1 per ally.\nAttached ally gets +1 THW and +1 ATK.\n<b>Response</b>: After you attach "
       "Jet Bike to an ally, ready that ally."),
    # ----------------------------------------------------------------------------------------------- Protection (118-126)
    _a("sy042", "* Kalyx", "", "4", "3", "1*", "1*", "R", "Protection", ["STARJAMMER"],
       "<b>Forced Response</b>: After Kalyx enters play, find Thorn Crew and put it into play.\n[star] <b>Response</b>: After Kalyx "
       "uses a basic power, put the top card of your deck into play facedown as a [[THORN]] ally."),
    _c("sy043", "Support", "Thorn Crew",
       {"RES": "R", "Permanent": "1", "Class": "Protection", "Linked": "Kalyx"}, [],
       "Permanent. Linked (Kalyx).\nEach facedown [[THORN]] ally has a base THW of 1, a base ATK of 1 and base hit points of 1.\n"
       "<b>Forced Response</b>: After a [[THORN]] ally is defeated, place that card in its owner's discard pile."),
    _a("sy044", "* K-Zzat", "", "3", "3", "2*", "1*", "Y", "Protection", ["STARJAMMER"],
       "<b>Response</b>: After K-Zzat attacks an enemy, deal 1 damage to a friendly character → stun the attacked enemy.\n"
       "<i>\"Injustice is a constant in the universe. Beings are different, but the concept is the same.\"</i>"),
    _a("sy045", "* Tolo Hawk", "", "2", "2", "1*", "1*", "R", "Protection", ["STARJAMMER"],
       "<b>Response</b>: After Tolo Hawk enters play, ready a friendly [[STARJAMMER]] character.\n"
       "<i>\"I worked so hard for this uniform. Thowing it away is like shedding my old life.\"</i>"),
    _c("sy046", "Event", "Ready for Anything",
       {"Cost": "3", "RES": "B", "Requirement": "YBR", "Class": "Protection"}, ["CONDITION"],
       REQ + "\n<b>Hero Action</b>: Stun and confuse an enemy. Give your identity a tough status card.\n"
       "<i>\"Bring it you snot nosed punk!\"</i> —Polaris"),
    _c("sy047", "Event", "Reckless Defense",
       {"Cost": "0", "RES": "R", "Class": "Protection"}, ["DEFENSE"],
       "<b>Hero Interrupt</b> <i>(defense)</i>: When a character would take damage from an attack, discard the top card of the encounter "
       "deck. Deal 1 damage to your identity for each icon " + ICONES + " in that card's boost area → prevent all damage from that attack."),
    _c("sy048", "Event", "Rogue Heroics",
       {"Cost": "2", "RES": "R", "Class": "Protection", "Alliance": "1"}, ["ATTACK"],
       "Alliance.\n<b>Hero Action</b> <i>(attack)</i>: Exhaust a [[STARJAMMER]] character and a [[GUARDIAN]] character → deal X damage "
       "among enemies in play, where X is the combined ATK of the two exhausted characters. Stun each character damaged this way."),
    _c("sy049", "Upgrade", "Armored Space Suit",
       {"Cost": "1", "RES": "R", "MaxPerUnit": "1", "Class": "Protection"}, ["ARMOR", "TECH"],
       "Attach to a [[STARJAMMER]] ally. Max 1 per ally.\nAttached ally gains the [[AERIAL]] trait.\n<b>Response</b>: After this card "
       "enters play, give the attached ally a tough status card."),
    _c("sy050", "Upgrade", "Plasnet Launcher",
       {"Cost": "1*", "RES": "B", "Restricted": "1", "Uses": "3,charge", "Class": "Protection"}, ["TECH", "WEAPON"],
       "Restricted. Uses (3 charge counters).\n<b>Action</b>: Exhaust Plasnet Launcher and remove 1 charge counter from it → the villain "
       "gets -1 ATK until the end of the round."),
]


# Gabarit d'allie FACE CACHEE de Kalyx (sy042) : « put the top card of your deck into play facedown as a THORN ally » (modele :
# `ultron_facedown_drone`, pack core). Valeurs de base donnees par Thorn Crew : THW 1, ATK 1, PV 1.
GABARIT_THORN = {"card_id": "sy_thorn_ally", "pic_id": "player", "type": "Ally", "name": "Thorn Ally", "subtitle": "",
                 "desc": {"HP": "1", "ATK": "1", "THW": "1"}, "traits": ["THORN"], "set_name": ""}


def verifier():
    ids = [c["card_id"] for c in CARTES_SY]
    assert ids == [f"sy{n:03d}" for n in range(1, 51)], "numerotation sy001-sy050 continue et dans l'ordre"
    for c in CARTES_SY:
        assert c["desc"].get("Class") in ("Basic", "Aggression", "Justice", "Leadership", "Protection"), c["card_id"]
        assert c["desc"].get("RES"), c["card_id"]
    par_classe = {}
    for c in CARTES_SY:
        par_classe[c["desc"]["Class"]] = par_classe.get(c["desc"]["Class"], 0) + 1
    assert par_classe == {"Basic": 15, "Aggression": 9, "Justice": 8, "Leadership": 9, "Protection": 9}, par_classe


def main():
    verifier()
    if "--ecrire" not in sys.argv:
        print(f"{len(CARTES_SY)} cartes valides (sy001-sy050). Ajouter --ecrire pour ecrire data/cards.json.")
        return 0
    with open(VERROU, "w") as verrou:
        fcntl.flock(verrou, fcntl.LOCK_EX)
        texte = io.open(CARTES, encoding="utf-8", newline="").read()
        donnees = json.loads(texte)
        avant = donnees.get(PACK)
        donnees[PACK] = CARTES_SY + [GABARIT_THORN]
        sortie = json.dumps(donnees, ensure_ascii=False, indent=1)
        tmp = CARTES + ".tmp-sy"
        io.open(tmp, "w", encoding="utf-8", newline="").write(sortie)
        os.replace(tmp, CARTES)
        print(f"data/cards.json : {PACK} {'remplace' if avant else 'cree'} ({len(CARTES_SY)} cartes). "
              f"Recalculer le checksum : tools/recalculer_checksums.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
